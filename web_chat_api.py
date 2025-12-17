"""
🌐 Web 對話界面後端 API

提供語音對話的 Web API 端點
"""

import os
import uuid
import time
from pathlib import Path
from typing import Optional, Dict
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# 導入模組
import sys
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.llm_emotion_router import llm_emotion_route
from modules.autonomous_emotion import autonomous_emotion_route, get_global_agent
from modules.speech_tag_mapper import extract_tags_from_text, map_tags_to_voice_settings
from modules.soft_ling import (
    process_with_soft_ling,
    detect_soft_ling_invocation,
    get_soft_ling_opening,
    generate_soft_ling_reply,
)
from eleven_tts import generate_speech, API_KEY, VOICE_ID
import requests

app = FastAPI(
    title="黃蓉語音對話系統 Web API",
    description="提供語音對話的 Web 界面 API",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設定目錄
AUDIO_DIR = Path("public/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR = Path("web_static")
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# 掛載靜態檔案
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    """對話請求模型"""
    text: str
    use_llm: bool = True
    provider: str = "openai"
    autonomy_mode: bool = True  # 是否使用自主模式
    autonomy_level: float = 0.7  # 自主程度（0.0-1.0）
    use_soft_ling: bool = True  # 是否使用花小軟模式


class ChatResponse(BaseModel):
    """對話回應模型"""
    status: str
    text: str
    tagged_text: str
    audio_url: str
    message: str
    autonomy_stats: Optional[Dict] = None  # 自主決策統計（可選）
    is_invocation: bool = False  # 是否為召喚咒語
    agent_name: str = "黃蓉"  # 代理名稱
    opening: Optional[str] = None  # 開靈語（可選）


@app.get("/")
async def root():
    """重定向到對話頁面"""
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    處理對話請求
    
    流程：文字 → 語氣判斷 → 語音產生
    """
    try:
        # 檢查是否為花小軟召喚咒語
        is_invocation = detect_soft_ling_invocation(request.text) if request.use_soft_ling else False

        # 產生回應文字（花小軟模式時才啟用 LLM）
        reply_text = request.text
        if request.use_soft_ling and request.use_llm:
            reply_text = generate_soft_ling_reply(request.text, provider=request.provider)

        # 1. 語氣判斷（花小軟模式優先）
        if request.use_soft_ling:
            # 使用花小軟模式
            soft_ling_result = process_with_soft_ling(
                reply_text,
                use_llm=request.use_llm
            )
            tagged_text = soft_ling_result["tagged_text"]
            voice_settings = soft_ling_result["voice_settings"]
        elif request.autonomy_mode:
            # 使用自主模式：小軟自己決定是否使用語氣
            agent = get_global_agent(autonomy_level=request.autonomy_level)
            tagged_text = autonomous_emotion_route(
                reply_text,
                autonomy_level=request.autonomy_level,
                use_llm=request.use_llm,
                agent=agent
            )
            # 提取標籤並映射到聲音參數
            tags = extract_tags_from_text(tagged_text)
            voice_settings = map_tags_to_voice_settings(tags)
        elif request.use_llm:
            # 傳統模式：使用 LLM 判斷
            tagged_text = llm_emotion_route(
                reply_text,
                provider=request.provider,
                fallback_to_rule=True
            )
            tags = extract_tags_from_text(tagged_text)
            voice_settings = map_tags_to_voice_settings(tags)
        else:
            # 規則式判斷
            from emotion_tag_engine import insert_emotion_tags
            tagged_text = insert_emotion_tags(reply_text)
            tags = extract_tags_from_text(tagged_text)
            voice_settings = map_tags_to_voice_settings(tags)
        
        # 2. 產生語音
        filename = f"chat_{uuid.uuid4().hex[:8]}.mp3"
        filepath = AUDIO_DIR / filename
        
        voice_id = VOICE_ID
        if not voice_id:
            raise HTTPException(status_code=500, detail="未設定 Voice ID")
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
        headers = {
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "model_id": "eleven_turbo_v2_5",
            "text": tagged_text,  # 保持標籤在文字中
            "voice_settings": voice_settings  # 使用映射的聲音參數
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"ElevenLabs API 錯誤：{response.text}"
            )
        
        # 3. 儲存音訊檔案
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        # 4. 回傳結果
        audio_url = f"/audio/{filename}"
        
        # 獲取自主決策統計（如果使用自主模式且非花小軟模式）
        autonomy_stats = None
        if request.autonomy_mode and not request.use_soft_ling:
            agent = get_global_agent(autonomy_level=request.autonomy_level)
            autonomy_stats = agent.get_autonomy_stats()
        
        # 如果是召喚咒語，添加開靈語標記
        response_data = {
            "status": "success",
            "text": reply_text,
            "tagged_text": tagged_text,
            "audio_url": audio_url,
            "message": "語音產生成功",
            "autonomy_stats": autonomy_stats,
            "is_invocation": is_invocation,
            "agent_name": "花小軟" if request.use_soft_ling else "黃蓉"
        }
        
        if is_invocation and request.use_soft_ling:
            response_data["opening"] = get_soft_ling_opening()
        
        return ChatResponse(**response_data)
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"❌ API 錯誤詳情:\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"發生錯誤：{str(e)}")


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """直接返回音訊流"""
    try:
        # 語氣判斷（自主模式或傳統模式）
        if request.autonomy_mode:
            agent = get_global_agent(autonomy_level=request.autonomy_level)
            tagged_text = autonomous_emotion_route(
                request.text,
                autonomy_level=request.autonomy_level,
                use_llm=request.use_llm,
                agent=agent
            )
        elif request.use_llm:
            tagged_text = llm_emotion_route(
                request.text,
                provider=request.provider,
                fallback_to_rule=True
            )
        else:
            from emotion_tag_engine import insert_emotion_tags
            tagged_text = insert_emotion_tags(request.text)
        
        # 呼叫 ElevenLabs API
        voice_id = VOICE_ID
        if not voice_id:
            raise HTTPException(status_code=500, detail="未設定 Voice ID")
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
        headers = {
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        }
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
        
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"ElevenLabs API 錯誤：{response.text}"
            )
        
        return StreamingResponse(
            response.iter_content(chunk_size=8192),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="huangrong_chat.mp3"'
            }
        )
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"❌ API 錯誤詳情:\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"發生錯誤：{str(e)}")


@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    """提供音訊檔案下載"""
    filepath = AUDIO_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="檔案不存在")
    
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
    uvicorn.run(app, host="0.0.0.0", port=8001)

