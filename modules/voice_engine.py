"""
🎤 語音引擎整合範例

展示如何整合自主語氣判斷、標籤映射和 TTS 生成
支援多語模式自動切換
"""

from modules.autonomous_emotion import autonomous_emotion_route, get_global_agent
from modules.speech_tag_mapper import extract_tags_from_text, map_tags_to_voice_settings
from eleven_tts import generate_speech
from typing import Optional
import re


# 語言檢測關鍵字
LANGUAGE_KEYWORDS = {
    "zh": {
        "keywords": ["你好", "謝謝", "再見", "是的", "不是", "什麼", "怎麼", "為什麼"],
        "model_id": "eleven_multilingual_v3"  # 支援中文
    },
    "en": {
        "keywords": ["hello", "thank", "goodbye", "yes", "no", "what", "how", "why"],
        "model_id": "eleven_turbo_v2_5"  # 英文優化
    },
    "ja": {
        "keywords": ["こんにちは", "ありがとう", "さようなら", "はい", "いいえ", "何", "どう", "なぜ"],
        "model_id": "eleven_multilingual_v3"  # 支援日文
    },
    "ko": {
        "keywords": ["안녕", "감사", "안녕히", "예", "아니", "무엇", "어떻게", "왜"],
        "model_id": "eleven_multilingual_v3"  # 支援韓文
    }
}


def detect_language(text: str) -> str:
    """
    自動檢測文字語言
    
    Args:
        text: 輸入文字
        
    Returns:
        語言代碼：zh, en, ja, ko，預設返回 "zh"
    """
    text_lower = text.lower()
    
    # 計算各語言的匹配分數
    scores = {}
    for lang_code, lang_info in LANGUAGE_KEYWORDS.items():
        score = sum(1 for keyword in lang_info["keywords"] if keyword.lower() in text_lower)
        scores[lang_code] = score
    
    # 檢查中文字符（CJK 統一漢字範圍）
    cjk_pattern = re.compile(r'[\u4e00-\u9fff]')
    if cjk_pattern.search(text):
        scores["zh"] = scores.get("zh", 0) + 10  # 大幅提高中文分數
    
    # 檢查日文假名
    hiragana_pattern = re.compile(r'[\u3040-\u309f]')
    katakana_pattern = re.compile(r'[\u30a0-\u30ff]')
    if hiragana_pattern.search(text) or katakana_pattern.search(text):
        scores["ja"] = scores.get("ja", 0) + 10
    
    # 檢查韓文
    korean_pattern = re.compile(r'[\uac00-\ud7a3]')
    if korean_pattern.search(text):
        scores["ko"] = scores.get("ko", 0) + 10
    
    # 返回分數最高的語言
    if scores:
        detected_lang = max(scores.items(), key=lambda x: x[1])[0]
        if scores[detected_lang] > 0:
            return detected_lang
    
    # 預設返回中文
    return "zh"


def get_model_id_for_language(lang: str) -> str:
    """
    根據語言獲取對應的模型 ID
    
    Args:
        lang: 語言代碼
        
    Returns:
        模型 ID
    """
    return LANGUAGE_KEYWORDS.get(lang, LANGUAGE_KEYWORDS["zh"])["model_id"]


def speak_with_autonomous_emotion(
    text: str,
    autonomy_level: float = 0.7,
    use_llm: bool = True,
    output_filename: str = "output.mp3",
    auto_detect_language: bool = True,
    language: Optional[str] = None,
    intensity: Optional[float] = None
) -> bool:
    """
    完整的語音生成流程：
    1. 自主語氣判斷
    2. 標籤映射到聲音參數
    3. TTS 生成
    
    Args:
        text: 輸入文字
        autonomy_level: 自主程度
        use_llm: 是否使用 LLM
        output_filename: 輸出檔案名稱
        
    Returns:
        成功返回 True
    """
    print(f"📝 輸入文字：{text}")
    
    # 1. 自主語氣判斷
    agent = get_global_agent(autonomy_level=autonomy_level)
    tagged_text = autonomous_emotion_route(
        text,
        autonomy_level=autonomy_level,
        use_llm=use_llm,
        agent=agent
    )
    
    print(f"🏷️  標籤後文字：{tagged_text}")
    
    # 2. 提取標籤並映射到聲音參數
    tags = extract_tags_from_text(tagged_text)
    voice_settings = map_tags_to_voice_settings(tags)
    
    print(f"🎵 聲音設定：{voice_settings}")
    
    # 3. 生成語音（使用映射的聲音參數）
    success = generate_speech(
        text=tagged_text,  # 保持標籤在文字中（ElevenLabs 會處理）
        filename=output_filename,
        use_tag_mapper=False,  # 已經手動映射，不需要再次映射
        voice_settings=voice_settings  # 使用映射的參數
    )
    
    if success:
        print(f"✅ 語音已生成：{output_filename}")
        return True
    else:
        print("❌ 語音生成失敗")
        return False


def analyze_emotion(text: str) -> dict:
    """
    分析文字的情緒（與用戶提供的範例格式一致）
    
    Args:
        text: 輸入文字
        
    Returns:
        {"text": "...", "tags": [...]}
    """
    agent = get_global_agent()
    tagged_text = agent.process_text(text, use_llm=True)
    tags = extract_tags_from_text(tagged_text)
    
    # 移除標籤，只保留純文字
    clean_text = re.sub(r'\[([^\]]+)\]\s*', '', tagged_text).strip()
    
    return {
        "text": clean_text,
        "tags": tags
    }


# 測試函數
if __name__ == "__main__":
    print("=" * 60)
    print("🎤 語音引擎整合測試（多語模式）")
    print("=" * 60)
    print()
    
    # 測試案例（多語言）
    test_cases = [
        ("你知道嗎？我真的好感動。", "zh"),
        ("Hello, how are you?", "en"),
        ("こんにちは、元気ですか？", "ja"),
        ("안녕하세요, 어떻게 지내세요?", "ko"),
    ]
    
    for text, expected_lang in test_cases:
        print(f"\n測試：{text}")
        print("-" * 60)
        
        # 語言檢測
        detected_lang = detect_language(text)
        model_id = get_model_id_for_language(detected_lang)
        print(f"檢測語言：{detected_lang}（預期：{expected_lang}）")
        print(f"使用模型：{model_id}")
        
        # 分析情緒
        emotion_result = analyze_emotion(text)
        print(f"分析結果：{emotion_result}")
        
        # 生成語音（可選，需要 API Key）
        # speak_with_autonomous_emotion(
        #     text,
        #     output_filename=f"test_{detected_lang}.mp3",
        #     auto_detect_language=True
        # )

