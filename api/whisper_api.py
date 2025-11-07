"""FastAPI WebSocket endpoint for streaming audio to Whisper."""

import logging
import os
import tempfile
from pathlib import Path
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from openai import OpenAI


router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")
SERVICE_API_KEY = os.getenv("SERVICE_API_KEY")
CHUNK_THRESHOLD = 4  # number of MediaRecorder chunks (~2-4 seconds)

logger = logging.getLogger("voice_agent")

client: OpenAI | None = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


def _verify_service_key(websocket: WebSocket) -> bool:
    if not SERVICE_API_KEY:
        return True
    provided = (
        websocket.headers.get("Service-Api-Key")
        or websocket.headers.get("x-service-api-key")
        or websocket.query_params.get("service_api_key")
    )
    client_host = websocket.client.host if websocket.client else "unknown"
    if provided != SERVICE_API_KEY:
        logger.warning("whisper websocket api key invalid", extra={"client": client_host})
        return False
    logger.info("whisper websocket api key verified", extra={"client": client_host})
    return True


async def _transcribe_chunks(chunks: List[bytes]) -> str:
    """Persist chunks to a temp file and call Whisper transcription."""
    if not client:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_file:
        for chunk in chunks:
            tmp_file.write(chunk)
        temp_path = Path(tmp_file.name)

    try:
        with temp_path.open("rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file,
            )
        return response.text or ""
    finally:
        try:
            temp_path.unlink(missing_ok=True)
        except OSError:
            pass


@router.websocket("/api/whisper")
async def whisper_websocket(websocket: WebSocket):
    if not _verify_service_key(websocket):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    if not client:
        await websocket.send_json(
            {
                "type": "error",
                "message": "OPENAI_API_KEY 未設定，無法使用 Whisper 服務",
            }
        )
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return

    audio_chunks: List[bytes] = []

    try:
        await websocket.send_json({"type": "ready"})

        while True:
            message = await websocket.receive()

            if "bytes" in message and message["bytes"] is not None:
                audio_chunks.append(message["bytes"])

                if len(audio_chunks) >= CHUNK_THRESHOLD:
                    try:
                        text = await _transcribe_chunks(audio_chunks)
                        await websocket.send_json({"type": "final", "text": text})
                    except Exception as exc:  # noqa: BLE001
                        logger.error("whisper transcribe failed", exc_info=exc)
                        await websocket.send_json({"type": "error", "message": str(exc)})
                    finally:
                        audio_chunks.clear()

            elif message.get("type") == "websocket.disconnect":
                break

    except WebSocketDisconnect:
        pass
    finally:
        if audio_chunks:
            try:
                text = await _transcribe_chunks(audio_chunks)
                await websocket.send_json({"type": "final", "text": text})
            except Exception:
                pass
        audio_chunks.clear()

