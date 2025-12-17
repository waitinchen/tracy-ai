"""
📡 ElevenLabs v3 語音 API 調用模組

使用 ElevenLabs v3 (alpha) API 產生語音輸出。
"""

import requests
import os
from dotenv import load_dotenv
from typing import Optional, Dict

# 載入環境變數
load_dotenv()

API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("ELEVEN_HUANGRONG_ID")
BASE_URL = "https://api.elevenlabs.io/v1"


def generate_speech(
    text: str,
    filename: str = "huangrong_output.mp3",
    voice_id: Optional[str] = None,
    model_id: str = "eleven_turbo_v2_5",
    stability: Optional[float] = None,
    similarity_boost: Optional[float] = None,
    style: Optional[float] = None,
    use_speaker_boost: Optional[bool] = None,
    use_tag_mapper: bool = True,
    voice_settings: Optional[Dict] = None
) -> bool:
    """
    產生語音檔案
    
    Args:
        text: 要轉換的文字（可包含語氣標籤）
        filename: 輸出檔案名稱
        voice_id: 聲線 ID（預設使用環境變數中的 ELEVEN_HUANGRONG_ID）
        model_id: 模型 ID（預設為 eleven_turbo_v2_5）
        stability: 穩定性參數（0.0-1.0），如果為 None 且啟用映射器則自動生成
        similarity_boost: 相似度提升（0.0-1.0），如果為 None 且啟用映射器則自動生成
        style: 風格參數（0.0-1.0），如果為 None 且啟用映射器則自動生成
        use_speaker_boost: 是否使用說話者增強，如果為 None 且啟用映射器則自動生成
        use_tag_mapper: 是否使用標籤映射器自動調整聲音參數（預設 True）
        voice_settings: 完整的聲音設定字典（如果提供，會覆蓋其他參數）
        
    Returns:
        成功返回 True，失敗返回 False
        
    Examples:
        >>> generate_speech("你好，我是黃蓉", "output.mp3")
        True
        >>> generate_speech("[crying] 你知道嗎？", "output.mp3", use_tag_mapper=True)
        True
    """
    # 檢查 API Key
    if not API_KEY:
        print("❌ 錯誤：未設定 ELEVEN_API_KEY，請檢查 .env 檔案")
        return False
    
    # 使用提供的 voice_id 或環境變數中的預設值
    target_voice_id = voice_id or VOICE_ID
    if not target_voice_id:
        print("❌ 錯誤：未設定 ELEVEN_HUANGRONG_ID，請檢查 .env 檔案")
        return False
    
    # 如果啟用標籤映射器，處理標籤並生成聲音設定
    final_voice_settings = voice_settings
    
    if use_tag_mapper and final_voice_settings is None:
        try:
            from modules.speech_tag_mapper import extract_tags_from_text, map_tags_to_voice_settings
            
            # 從文字中提取標籤
            tags = extract_tags_from_text(text)
            
            # 生成聲音設定
            auto_settings = map_tags_to_voice_settings(tags)
            
            # 如果參數未提供，使用自動生成的
            final_voice_settings = {
                "stability": stability if stability is not None else auto_settings["stability"],
                "similarity_boost": similarity_boost if similarity_boost is not None else auto_settings["similarity_boost"],
                "style": style if style is not None else auto_settings["style"],
                "use_speaker_boost": use_speaker_boost if use_speaker_boost is not None else auto_settings["use_speaker_boost"]
            }
            
        except ImportError:
            # 如果映射器不可用，使用預設值
            final_voice_settings = None
    
    # 如果沒有生成設定，使用提供的參數或預設值
    if final_voice_settings is None:
        final_voice_settings = {
            "stability": stability if stability is not None else 0.4,
            "similarity_boost": similarity_boost if similarity_boost is not None else 0.8,
            "style": style if style is not None else 0.9,
            "use_speaker_boost": use_speaker_boost if use_speaker_boost is not None else True
        }
    
    try:
        # 發送請求
        print(f"🔄 正在產生語音...")
        print(f"📝 文字內容：{text[:50]}..." if len(text) > 50 else f"📝 文字內容：{text}")
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            # 儲存音訊檔案
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filename) / 1024  # KB
            print(f"✅ 語音已儲存為：{filename} ({file_size:.2f} KB)")
            return True
        else:
            print(f"❌ 發生錯誤：{response.status_code}")
            print(f"錯誤訊息：{response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 網路請求錯誤：{str(e)}")
        return False
    except Exception as e:
        print(f"❌ 發生未預期的錯誤：{str(e)}")
        return False


def get_voice_info(voice_id: Optional[str] = None) -> Optional[dict]:
    """
    取得聲線資訊
    
    Args:
        voice_id: 聲線 ID（預設使用環境變數中的值）
        
    Returns:
        聲線資訊字典，失敗返回 None
    """
    if not API_KEY:
        print("❌ 錯誤：未設定 ELEVEN_API_KEY")
        return None
    
    target_voice_id = voice_id or VOICE_ID
    if not target_voice_id:
        print("❌ 錯誤：未設定 voice_id")
        return None
    
    url = f"{BASE_URL}/voices/{target_voice_id}"
    headers = {"xi-api-key": API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 無法取得聲線資訊：{response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 錯誤：{str(e)}")
        return None


def list_available_voices() -> Optional[list]:
    """
    列出所有可用的聲線
    
    Returns:
        聲線列表，失敗返回 None
    """
    if not API_KEY:
        print("❌ 錯誤：未設定 ELEVEN_API_KEY")
        return None
    
    url = f"{BASE_URL}/voices"
    headers = {"xi-api-key": API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("voices", [])
        else:
            print(f"❌ 無法取得聲線列表：{response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 錯誤：{str(e)}")
        return None

