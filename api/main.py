"""
🚀 FastAPI 後端 API：黃蓉語音系統對外接口

提供 REST API 供外部系統調用，支援：
- POST /api/voice/huangrong - 產生語音並回傳 URL
- POST /api/voice/huangrong/stream - 直接返回音訊流
"""

import asyncio
import logging
import os
import time
from pathlib import Path
from typing import Dict, Optional

import requests
from fastapi import Depends, FastAPI, HTTPException, Request, Header
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# 導入模組
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.llm_emotion_router import llm_emotion_route
from modules.speech_tag_mapper import extract_tags_from_text
from modules.voice_cache_engine import (
    ensure_cache_dir,
    generate_audio_key,
    get_cached_audio_path,
    is_cache_valid,
    clean_expired_cache,
)
from eleven_tts import generate_speech, API_KEY, VOICE_ID

from .whisper_api import router as whisper_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice_agent")

SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_TRACES_SAMPLE_RATE = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0"))

if SENTRY_DSN:
    try:
        import sentry_sdk

        sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE)
        logger.info("Sentry initialized")
    except ImportError:
        logger.warning("sentry-sdk 未安裝，無法初始化 Sentry")


app = FastAPI(
    title="黃蓉語音系統 API",
    description="ElevenLabs v3 語音合成 API，支援自動語氣標籤",
    version="2.0.0"
)

app.include_router(whisper_router)

# CORS 設定（允許前端調用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境請設定特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設定音訊儲存目錄
AUDIO_DIR = Path("public/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
SERVICE_API_KEY = os.getenv("SERVICE_API_KEY")
RATE_LIMIT_PER_MIN = int(os.getenv("SERVICE_RATE_LIMIT_PER_MIN", "60"))
ELEVEN_MAX_RETRIES = int(os.getenv("ELEVEN_MAX_RETRIES", "3"))
ELEVEN_RETRY_BACKOFF = float(os.getenv("ELEVEN_RETRY_BACKOFF", "1.5"))

_rate_state: Dict[str, tuple[int, int]] = {}
_rate_lock = asyncio.Lock()

ensure_cache_dir()


class VoiceRequest(BaseModel):
    """語音請求模型"""
    text: str
    provider: Optional[str] = "openai"  # LLM provider: "openai" 或 "anthropic"
    emotion_auto: Optional[bool] = True  # 是否自動判斷語氣
    voice_id: Optional[str] = None  # 可選：指定不同的 voice_id


class VoiceResponse(BaseModel):
    """語音回應模型"""
    status: str
    audio_url: Optional[str] = None
    text: Optional[str] = None
    tagged_text: Optional[str] = None
    voice_tags: Optional[list[str]] = None
    cache_hit: Optional[bool] = None
    message: Optional[str] = None


async def verify_api_key(request: Request, service_api_key: Optional[str] = Header(None, alias="Service-Api-Key")) -> None:
    """Verify client provided service API key."""
    if not SERVICE_API_KEY:
        return

    provided = (
        service_api_key
        or request.headers.get("x-service-api-key")
        or request.query_params.get("service_api_key")
    )

    client_host = request.client.host if request.client else "unknown"

    if provided != SERVICE_API_KEY:
        logger.warning(
            "service api key invalid",
            extra={"path": request.url.path, "client": client_host},
        )
        raise HTTPException(status_code=401, detail="Invalid Service API Key")

    logger.info(
        "service api key verified",
        extra={"path": request.url.path, "client": client_host},
    )


async def enforce_rate_limit(request: Request) -> None:
    if RATE_LIMIT_PER_MIN <= 0:
        return

    identifier = request.headers.get("x-service-api-key") or (request.client.host if request.client else "anonymous")
    current_bucket = int(time.time() // 60)

    async with _rate_lock:
        count, bucket = _rate_state.get(identifier, (0, current_bucket))
        if bucket != current_bucket:
            count = 0
            bucket = current_bucket

        if count >= RATE_LIMIT_PER_MIN:
            logger.warning("Rate limit exceeded", extra={"client": identifier, "path": request.url.path})
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        _rate_state[identifier] = (count + 1, bucket)


def call_elevenlabs_generate(payload: dict, voice_id: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    retry_wait = ELEVEN_RETRY_BACKOFF
    last_error: Optional[Exception] = None

    for attempt in range(1, ELEVEN_MAX_RETRIES + 1):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response
            last_error = HTTPException(status_code=response.status_code, detail=f"ElevenLabs API 錯誤：{response.text}")
            logger.warning("ElevenLabs call failed", extra={"attempt": attempt, "status": response.status_code})
        except requests.RequestException as exc:  # noqa: BLE001
            last_error = exc
            logger.error("ElevenLabs request exception", exc_info=exc, extra={"attempt": attempt})

        if attempt < ELEVEN_MAX_RETRIES:
            time.sleep(retry_wait)
            retry_wait *= 2

    if isinstance(last_error, HTTPException):
        raise last_error
    if isinstance(last_error, Exception):
        raise HTTPException(status_code=502, detail=str(last_error))
    raise HTTPException(status_code=502, detail="ElevenLabs API 錯誤")


def call_elevenlabs_stream(payload: dict, voice_id: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    retry_wait = ELEVEN_RETRY_BACKOFF
    last_exc: Optional[Exception] = None

    for attempt in range(1, ELEVEN_MAX_RETRIES + 1):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30, stream=True)
            if response.status_code == 200:
                return response
            logger.warning("ElevenLabs stream failed", extra={"attempt": attempt, "status": response.status_code})
        except requests.RequestException as exc:  # noqa: BLE001
            last_exc = exc
            logger.error("ElevenLabs stream exception", exc_info=exc, extra={"attempt": attempt})

        if attempt < ELEVEN_MAX_RETRIES:
            time.sleep(retry_wait)
            retry_wait *= 2

    if last_exc:
        raise last_exc
    raise HTTPException(status_code=502, detail="ElevenLabs stream 呼叫失敗")


@app.get("/")
async def root():
    """根路徑"""
    return {
        "message": "黃蓉語音系統 API v2.0",
        "endpoints": {
            "POST /api/voice/huangrong": "產生語音並回傳 URL",
            "POST /api/voice/huangrong/stream": "直接返回音訊流"
        }
    }


@app.post(
    "/api/voice/huangrong",
    response_model=VoiceResponse,
    dependencies=[Depends(verify_api_key), Depends(enforce_rate_limit)],
)
async def generate_voice_api(request: VoiceRequest, http_request: Request):
    """
    產生語音並回傳下載 URL
    
    範例請求：
    ```json
    {
        "text": "你今天看起來心情不錯唷～",
        "provider": "openai",
        "emotion_auto": true
    }
    ```
    """
    try:
        # 1. 判斷語氣（如果需要）
        if request.emotion_auto:
            tagged_text = llm_emotion_route(
                request.text,
                provider=request.provider,
                fallback_to_rule=True
            )
        else:
            tagged_text = request.text

        voice_id = request.voice_id or VOICE_ID
        if not voice_id:
            raise HTTPException(status_code=500, detail="未設定 Voice ID")

        tags = extract_tags_from_text(tagged_text)
        cache_key = generate_audio_key(request.text, voice_id, tags)
        cache_path = get_cached_audio_path(cache_key)
        cache_hit = is_cache_valid(cache_path)

        if cache_hit:
            audio_filename = cache_path.name
            audio_url = f"{BASE_URL}/audio/{audio_filename}"
            logger.info(
                "voice cache hit",
                extra={
                    "path": http_request.url.path,
                    "cache_hit": True,
                    "tags": tags,
                    "text_preview": request.text[:40],
                },
            )
            return VoiceResponse(
                status="success",
                audio_url=audio_url,
                text=request.text,
                tagged_text=tagged_text,
                voice_tags=tags,
                cache_hit=True,
                message="語音產生成功（快取）"
            )

        # 2. 呼叫 ElevenLabs API（含重試）
        payload = {
            "model_id": "eleven_turbo_v2_5",
            "text": tagged_text,
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.8,
                "style": 0.9,
                "use_speaker_boost": True
            }
        }
        try:
            start_time = time.time()
            response = call_elevenlabs_generate(payload, voice_id)
            elapsed = time.time() - start_time
            with open(cache_path, "wb") as f:
                f.write(response.content)

            audio_url = f"{BASE_URL}/audio/{cache_path.name}"
            clean_expired_cache()

            logger.info(
                "voice generated",
                extra={
                    "path": http_request.url.path,
                    "cache_hit": False,
                    "elevenlabs_latency_ms": int(elapsed * 1000),
                    "tags": tags,
                    "text_preview": request.text[:40],
                },
            )

            return VoiceResponse(
                status="success",
                audio_url=audio_url,
                text=request.text,
                tagged_text=tagged_text,
                voice_tags=tags,
                cache_hit=False,
                message="語音產生成功"
            )

        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            logger.error("ElevenLabs 產生語音失敗，改用 fallback", exc_info=exc)
            return VoiceResponse(
                status="fallback",
                audio_url=None,
                text=request.text,
                tagged_text=tagged_text,
                voice_tags=tags,
                cache_hit=False,
                message="語音服務暫時不可用，小軟改以文字回覆"
            )
        
    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        logger.exception("generate_voice_api 發生未預期錯誤")
        raise HTTPException(status_code=500, detail=f"發生錯誤：{str(e)}")


@app.post(
    "/api/voice/huangrong/stream",
    dependencies=[Depends(verify_api_key), Depends(enforce_rate_limit)],
)
async def generate_voice_stream(request: VoiceRequest, http_request: Request):
    """直接返回音訊流（Streaming Response）。"""
    try:
        if request.emotion_auto:
            tagged_text = llm_emotion_route(
                request.text,
                provider=request.provider,
                fallback_to_rule=True
            )
        else:
            tagged_text = request.text

        voice_id = request.voice_id or VOICE_ID
        if not voice_id:
            raise HTTPException(status_code=500, detail="未設定 Voice ID")

        payload = {
            "model_id": "eleven_turbo_v2_5",
            "text": tagged_text,
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.8,
                "style": 0.9,
                "use_speaker_boost": True
            }
        }

        try:
            start_time = time.time()
            response = call_elevenlabs_stream(payload, voice_id)
            elapsed = time.time() - start_time
            logger.info(
                "voice stream generated",
                extra={
                    "path": http_request.url.path,
                    "elevenlabs_latency_ms": int(elapsed * 1000),
                    "tags": extract_tags_from_text(tagged_text),
                },
            )

            return StreamingResponse(
                response.iter_content(chunk_size=8192),
                media_type="audio/mpeg",
                headers={
                    "Content-Disposition": f'attachment; filename="huangrong_audio.mp3"'
                }
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("ElevenLabs stream 生成失敗", exc_info=exc)
            raise HTTPException(status_code=502, detail="語音服務暫時不可用")

    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        logger.exception("generate_voice_stream 發生未預期錯誤")
        raise HTTPException(status_code=500, detail=f"發生錯誤：{str(e)}")


@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    """提供音訊檔案下載"""
    filepath = AUDIO_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="檔案不存在")
    
    from fastapi.responses import FileResponse
    return FileResponse(filepath, media_type="audio/mpeg")


@app.get("/health")
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "api_key_set": bool(API_KEY),
        "voice_id_set": bool(VOICE_ID)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

