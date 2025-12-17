"""
🎵 語氣標籤 → ElevenLabs 聲音參數映射層

將語氣標籤轉換為 ElevenLabs API 的聲音設定參數
"""

from typing import List, Dict, Optional
import math


# ElevenLabs v3 支援的語氣標籤
EMOTION_TAGS = [
    "excited", "whispers", "sarcastic", "curious", "softly", "crying",
    "starts laughing", "sings", "angry", "playful", "speaks quickly",
    "sighs", "happy", "sad", "surprised", "whispering", "echoes",
]


def map_tags_to_voice_settings(
    tags: List[str],
    base_stability: float = 0.4,
    base_similarity_boost: float = 0.8,
    base_style: float = 0.9,
    intensity: Optional[float] = None
) -> Dict[str, float]:
    """
    將語氣標籤轉換為 ElevenLabs voice_settings 參數
    
    Args:
        tags: 語氣標籤列表，例如 ["crying", "curious"]
        base_stability: 基礎穩定性（0.0-1.0）
        base_similarity_boost: 基礎相似度提升（0.0-1.0）
        base_style: 基礎風格（0.0-1.0）
        intensity: 語氣強度（0.0-1.0），如果為 None 則根據標籤自動計算
        
    Returns:
        voice_settings 字典，包含 stability, similarity_boost, style, use_speaker_boost, intensity
    """
    if not tags:
        return {
            "stability": base_stability,
            "similarity_boost": base_similarity_boost,
            "style": base_style,
            "use_speaker_boost": True,
            "intensity": intensity if intensity is not None else 0.5
        }
    
    # 語氣標籤到聲音參數的映射（包含強度基礎值）
    tag_mappings = {
        # 情緒強烈 → 降低穩定性，提高風格表現，高強度
        "crying": {
            "stability": 0.3,
            "similarity_boost": 0.7,
            "style": 0.95,
            "use_speaker_boost": True,
            "intensity": 0.9  # 高強度
        },
        "angry": {
            "stability": 0.35,
            "similarity_boost": 0.75,
            "style": 0.95,
            "use_speaker_boost": True,
            "intensity": 0.95  # 極高強度
        },
        "excited": {
            "stability": 0.5,
            "similarity_boost": 0.85,
            "style": 0.95,
            "use_speaker_boost": True,
            "intensity": 0.85  # 高強度
        },
        "happy": {
            "stability": 0.45,
            "similarity_boost": 0.8,
            "style": 0.9,
            "use_speaker_boost": True,
            "intensity": 0.75  # 中高強度
        },
        
        # 輕柔/安靜 → 降低穩定性，降低風格，低強度
        "whispers": {
            "stability": 0.25,
            "similarity_boost": 0.6,
            "style": 0.7,
            "use_speaker_boost": False,
            "intensity": 0.2  # 低強度
        },
        "whispering": {
            "stability": 0.25,
            "similarity_boost": 0.6,
            "style": 0.7,
            "use_speaker_boost": False,
            "intensity": 0.2  # 低強度
        },
        "softly": {
            "stability": 0.3,
            "similarity_boost": 0.65,
            "style": 0.75,
            "use_speaker_boost": False,
            "intensity": 0.3  # 低強度
        },
        
        # 調皮/活潑 → 中等穩定性，高風格，中高強度
        "playful": {
            "stability": 0.5,
            "similarity_boost": 0.85,
            "style": 0.9,
            "use_speaker_boost": True,
            "intensity": 0.7  # 中高強度
        },
        "curious": {
            "stability": 0.45,
            "similarity_boost": 0.8,
            "style": 0.85,
            "use_speaker_boost": True,
            "intensity": 0.6  # 中等強度
        },
        
        # 快速/急促 → 提高穩定性，高風格，高強度
        "speaks quickly": {
            "stability": 0.6,
            "similarity_boost": 0.85,
            "style": 0.9,
            "use_speaker_boost": True,
            "intensity": 0.8  # 高強度
        },
        
        # 悲傷 → 低穩定性，中等風格，中強度
        "sad": {
            "stability": 0.3,
            "similarity_boost": 0.7,
            "style": 0.8,
            "use_speaker_boost": True,
            "intensity": 0.5  # 中等強度
        },
        
        # 驚訝 → 低穩定性，高風格，高強度
        "surprised": {
            "stability": 0.35,
            "similarity_boost": 0.8,
            "style": 0.95,
            "use_speaker_boost": True,
            "intensity": 0.85  # 高強度
        },
        
        # 特殊效果
        "sighs": {
            "stability": 0.25,
            "similarity_boost": 0.6,
            "style": 0.7,
            "use_speaker_boost": False,
            "intensity": 0.3  # 低強度
        },
        "starts laughing": {
            "stability": 0.4,
            "similarity_boost": 0.8,
            "style": 0.9,
            "use_speaker_boost": True,
            "intensity": 0.8  # 高強度
        },
        "sings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.85,
            "use_speaker_boost": True,
            "intensity": 0.7  # 中高強度
        },
        "sarcastic": {
            "stability": 0.45,
            "similarity_boost": 0.8,
            "style": 0.85,
            "use_speaker_boost": True,
            "intensity": 0.65  # 中高強度
        },
        "echoes": {
            "stability": 0.4,
            "similarity_boost": 0.7,
            "style": 0.8,
            "use_speaker_boost": False,
            "intensity": 0.4  # 低中強度
        },
    }
    
    # 初始化結果
    result = {
        "stability": base_stability,
        "similarity_boost": base_similarity_boost,
        "style": base_style,
        "use_speaker_boost": True,
        "intensity": intensity if intensity is not None else 0.5
    }
    
    # 處理多個標籤：計算加權平均
    valid_tags = [tag for tag in tags if tag in tag_mappings]
    
    if not valid_tags:
        return result
    
    # 如果只有一個標籤，直接使用
    if len(valid_tags) == 1:
        result.update(tag_mappings[valid_tags[0]])
        # 如果提供了 intensity，覆蓋標籤的預設值
        if intensity is not None:
            result["intensity"] = intensity
        return result
    
    # 多個標籤：計算平均值（加權）
    # 情緒強烈的標籤權重更高
    strong_emotions = ["crying", "angry", "excited", "surprised"]
    
    weights = []
    settings_list = []
    
    for tag in valid_tags:
        weight = 1.5 if tag in strong_emotions else 1.0
        weights.append(weight)
        settings_list.append(tag_mappings[tag])
    
    total_weight = sum(weights)
    
    # 計算加權平均
    result["stability"] = sum(
        s["stability"] * w for s, w in zip(settings_list, weights)
    ) / total_weight
    
    result["similarity_boost"] = sum(
        s["similarity_boost"] * w for s, w in zip(settings_list, weights)
    ) / total_weight
    
    result["style"] = sum(
        s["style"] * w for s, w in zip(settings_list, weights)
    ) / total_weight
    
    # intensity: 計算加權平均，但如果提供了 intensity 參數則使用它
    if intensity is None:
        result["intensity"] = sum(
            s["intensity"] * w for s, w in zip(settings_list, weights)
        ) / total_weight
    else:
        result["intensity"] = intensity
    
    # use_speaker_boost: 如果任何標籤需要，就啟用
    result["use_speaker_boost"] = any(
        s["use_speaker_boost"] for s in settings_list
    )
    
    # 確保數值在有效範圍內
    result["stability"] = max(0.0, min(1.0, result["stability"]))
    result["similarity_boost"] = max(0.0, min(1.0, result["similarity_boost"]))
    result["style"] = max(0.0, min(1.0, result["style"]))
    result["intensity"] = max(0.0, min(1.0, result["intensity"]))
    
    return result


def extract_tags_from_text(text: str) -> List[str]:
    """
    從文字中提取語氣標籤
    
    Args:
        text: 可能包含標籤的文字，例如 "[crying][curious] 你知道嗎？"
        
    Returns:
        標籤列表，例如 ["crying", "curious"]
    """
    import re
    tags = []
    pattern = r'\[([^\]]+)\]'
    matches = re.findall(pattern, text)
    
    for match in matches:
        # 處理多詞標籤（如 "speaks quickly"）
        if match in EMOTION_TAGS:
            tags.append(match)
        # 嘗試匹配部分標籤
        else:
            # 檢查是否是已知標籤的變體
            match_lower = match.lower()
            for tag in EMOTION_TAGS:
                if tag.lower() == match_lower or tag.lower().replace(" ", "") == match_lower:
                    tags.append(tag)
                    break
    
    return tags


def process_text_with_voice_settings(
    text: str,
    tags: Optional[List[str]] = None,
    intensity: Optional[float] = None
) -> tuple[str, Dict[str, float]]:
    """
    處理文字並生成聲音設定
    
    Args:
        text: 原始文字或包含標籤的文字
        tags: 可選的標籤列表（如果為 None，會從文字中提取）
        intensity: 可選的語氣強度（0.0-1.0）
        
    Returns:
        (純文字, voice_settings) 元組
    """
    # 如果沒有提供標籤，從文字中提取
    if tags is None:
        tags = extract_tags_from_text(text)
        # 移除文字中的標籤
        import re
        clean_text = re.sub(r'\[([^\]]+)\]\s*', '', text).strip()
    else:
        clean_text = text
    
    # 生成聲音設定（包含 intensity）
    voice_settings = map_tags_to_voice_settings(tags, intensity=intensity)
    
    return clean_text, voice_settings


# 測試函數
if __name__ == "__main__":
    print("=" * 60)
    print("語氣標籤 → 聲音參數映射測試")
    print("=" * 60)
    print()
    
    test_cases = [
        (["crying", "curious"], "哭泣+好奇"),
        (["excited"], "興奮"),
        (["whispers"], "悄悄話"),
        (["playful"], "調皮"),
        (["angry"], "生氣"),
        ([], "無標籤"),
    ]
    
    for tags, description in test_cases:
        settings = map_tags_to_voice_settings(tags)
        print(f"{description}: {tags}")
        print(f"  穩定性: {settings['stability']:.2f}")
        print(f"  相似度: {settings['similarity_boost']:.2f}")
        print(f"  風格: {settings['style']:.2f}")
        print(f"  說話者增強: {settings['use_speaker_boost']}")
        print(f"  強度: {settings.get('intensity', 0.5):.2f}")
        print()
    
    # 測試強度調節
    print("=" * 60)
    print("強度調節測試")
    print("=" * 60)
    tags = ["excited"]
    for intensity in [0.3, 0.5, 0.7, 0.9]:
        settings = map_tags_to_voice_settings(tags, intensity=intensity)
        print(f"強度 {intensity:.1f}: {settings['intensity']:.2f}")
    
    # 測試文字提取
    test_text = "[crying][curious] 你知道嗎？我真的好感動。"
    clean_text, settings = process_text_with_voice_settings(test_text)
    print(f"文字: {test_text}")
    print(f"純文字: {clean_text}")
    print(f"聲音設定: {settings}")

