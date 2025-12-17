"""
🧪 語氣標籤插入模組（Emotion Tag Engine）

根據文字內容自動插入語氣標籤，讓黃蓉能夠根據語境表達不同情緒。
"""


def insert_emotion_tags(text: str) -> str:
    """
    根據關鍵字套用語氣標籤
    
    Args:
        text: 原始文字內容
        
    Returns:
        插入語氣標籤後的文字
        
    Examples:
        >>> insert_emotion_tags("你好")
        '[excited] 你好'
        
        >>> insert_emotion_tags("這是秘密")
        '[whispers] 這是秘密'
    """
    # 轉換為小寫以便比對（保留原始大小寫）
    text_lower = text.lower()
    
    # 興奮/開心情緒
    if any(keyword in text_lower for keyword in ["你好", "哈囉", "嗨", "hello", "hi", "太好了", "真棒"]):
        return "[excited] " + text
    
    # 悄悄話/秘密
    elif any(keyword in text_lower for keyword in ["秘密", "悄悄話", "偷偷", "不要告訴", "小聲"]):
        return "[whispers] " + text
    
    # 哭泣/難過
    elif any(keyword in text_lower for keyword in ["哭", "難過", "傷心", "悲傷", "眼淚", "嗚嗚"]):
        return "[crying][sighs] " + text
    
    # 生氣/憤怒
    elif any(keyword in text_lower for keyword in ["氣死我", "生氣", "憤怒", "討厭", "可惡"]):
        return "[angry] " + text
    
    # 好奇/疑問
    elif any(keyword in text_lower for keyword in ["你知道嗎", "你知道", "你知道", "為什麼", "怎麼", "什麼"]):
        return "[curious] " + text
    
    # 預設：快速/調皮（黃蓉的典型風格）
    else:
        return "[speaks quickly][playful] " + text


def insert_emotion_tags_advanced(text: str, emotion: str = None) -> str:
    """
    進階版本：可手動指定語氣標籤
    
    Args:
        text: 原始文字內容
        emotion: 手動指定的語氣標籤（可選）
        
    Returns:
        插入語氣標籤後的文字
    """
    if emotion:
        return f"[{emotion}] " + text
    
    return insert_emotion_tags(text)


# 可用的語氣標籤列表（ElevenLabs v3 alpha 支援）
AVAILABLE_EMOTION_TAGS = [
    "excited",      # 興奮
    "whispers",     # 悄悄話
    "crying",       # 哭泣
    "sighs",        # 嘆息
    "angry",        # 生氣
    "curious",      # 好奇
    "playful",      # 調皮
    "speaks quickly",  # 快速說話
    "sings",        # 唱歌
    "happy",        # 開心
    "sad",          # 難過
    "surprised",    # 驚訝
    "whispering",   # 低語
]


