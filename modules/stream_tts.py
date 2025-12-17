"""
🌊 ElevenLabs 即時串流播放模組

使用 WebSocket 實現即時語音串流播放
"""

import requests
import os
from dotenv import load_dotenv
from typing import Optional, Callable, Generator
import json

load_dotenv()

API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("ELEVEN_HUANGRONG_ID")
BASE_URL = "https://api.elevenlabs.io/v1"


def stream_speech(
    text: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_turbo_v2_5",
    voice_settings: Optional[dict] = None,
    chunk_size: int = 1024
) -> Generator[bytes, None, None]:
    """
    即時串流語音生成（使用 HTTP Streaming）
    
    Args:
        text: 要轉換的文字（可包含語氣標籤）
        voice_id: 聲線 ID（預設使用環境變數）
        model_id: 模型 ID
        voice_settings: 聲音設定字典
        chunk_size: 每次讀取的位元組數
        
    Yields:
        音訊資料塊（bytes）
        
    Examples:
        >>> for chunk in stream_speech("你好"):
        ...     audio_player.write(chunk)
    """
    if not API_KEY:
        raise ValueError("未設定 ELEVEN_API_KEY")
    
    target_voice_id = voice_id or VOICE_ID
    if not target_voice_id:
        raise ValueError("未設定 voice_id")
    
    if voice_settings is None:
        voice_settings = {
            "stability": 0.4,
            "similarity_boost": 0.8,
            "style": 0.9,
            "use_speaker_boost": True
        }
    
    url = f"{BASE_URL}/text-to-speech/{target_voice_id}/stream"
    
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model_id": model_id,
        "text": text,
        "voice_settings": voice_settings
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"API 錯誤：{response.status_code} - {response.text}")
        
        # 逐塊讀取音訊資料
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                yield chunk
                
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"網路錯誤：{str(e)}")


def stream_speech_to_file(
    text: str,
    filename: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_turbo_v2_5",
    voice_settings: Optional[dict] = None
) -> bool:
    """
    串流語音並儲存到檔案
    
    Args:
        text: 要轉換的文字
        filename: 輸出檔案名稱
        voice_id: 聲線 ID
        model_id: 模型 ID
        voice_settings: 聲音設定
        
    Returns:
        成功返回 True
    """
    try:
        with open(filename, "wb") as f:
            for chunk in stream_speech(text, voice_id, model_id, voice_settings):
                f.write(chunk)
        
        file_size = os.path.getsize(filename) / 1024
        print(f"✅ 語音已儲存為：{filename} ({file_size:.2f} KB)")
        return True
        
    except Exception as e:
        print(f"❌ 錯誤：{str(e)}")
        return False


def stream_speech_with_callback(
    text: str,
    callback: Callable[[bytes], None],
    voice_id: Optional[str] = None,
    model_id: str = "eleven_turbo_v2_5",
    voice_settings: Optional[dict] = None
) -> bool:
    """
    串流語音並使用回調函數處理每個資料塊
    
    Args:
        text: 要轉換的文字
        callback: 處理每個音訊塊的回調函數
        voice_id: 聲線 ID
        model_id: 模型 ID
        voice_settings: 聲音設定
        
    Returns:
        成功返回 True
        
    Examples:
        >>> def play_chunk(chunk):
        ...     audio_player.write(chunk)
        >>> stream_speech_with_callback("你好", play_chunk)
    """
    try:
        for chunk in stream_speech(text, voice_id, model_id, voice_settings):
            callback(chunk)
        return True
    except Exception as e:
        print(f"❌ 錯誤：{str(e)}")
        return False


# 測試函數
if __name__ == "__main__":
    print("=" * 60)
    print("即時串流播放測試")
    print("=" * 60)
    print()
    
    test_text = "你好，我是黃蓉！"
    print(f"測試文字：{test_text}")
    print("正在串流生成語音...")
    
    # 測試串流到檔案
    success = stream_speech_to_file(
        test_text,
        "stream_test.mp3",
        voice_settings={
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.9,
            "use_speaker_boost": True
        }
    )
    
    if success:
        print("✅ 串流測試成功")
    else:
        print("❌ 串流測試失敗")


