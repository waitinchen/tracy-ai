"""
🧠 LLM 語氣判斷器（GPT 自動標語氣）

使用 GPT/Claude 等 LLM 根據輸入文字語意，自動加上適合的 ElevenLabs v3 語氣標籤。
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# 支援多種 LLM Provider
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # 預設使用 gpt-4o-mini
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


# ElevenLabs v3 支援的語氣標籤
AVAILABLE_EMOTION_TAGS = [
    "excited",          # 興奮
    "whispers",         # 悄悄話
    "sarcastic",        # 諷刺
    "curious",          # 好奇
    "softly",           # 輕柔
    "crying",           # 哭泣
    "starts laughing",  # 開始笑
    "sings",            # 唱歌
    "angry",            # 生氣
    "playful",          # 調皮
    "speaks quickly",  # 快速說話
    "sighs",            # 嘆息
    "happy",            # 開心
    "sad",              # 難過
    "surprised",        # 驚訝
    "whispering",       # 低語
    "echoes",           # 回音
]


def create_emotion_prompt(text: str) -> str:
    """
    建立語氣判斷的 Prompt
    
    Args:
        text: 輸入文字
        
    Returns:
        Prompt 字串
    """
    prompt = f"""請根據輸入的句子判斷語氣，並插入最合適的 ElevenLabs 標籤。

可用的標籤包括：{', '.join([f'[{tag}]' for tag in AVAILABLE_EMOTION_TAGS])}

規則：
1. 根據語意和情感選擇最適合的標籤（可多個）
2. 標籤格式：[tag1][tag2] 文字內容
3. 如果不需要特殊語氣，直接返回原文字

範例：
輸入：你知道嗎？我真的好感動。
輸出：[crying][softly] 你知道嗎？我真的好感動。

輸入：太好了！我們成功了！
輸出：[excited][happy] 太好了！我們成功了！

輸入：這是個秘密，不要告訴別人。
輸出：[whispers] 這是個秘密，不要告訴別人。

現在請處理以下輸入：
輸入：{text}
輸出："""
    
    return prompt


def llm_emotion_route_openai(text: str, model: str = "gpt-4o-mini") -> Optional[str]:
    """
    使用 OpenAI API 判斷語氣
    
    Args:
        text: 輸入文字
        model: 使用的模型（預設 gpt-4o-mini）
        
    Returns:
        加上語氣標籤的文字，失敗返回 None
    """
    try:
        import openai
        
        if not OPENAI_API_KEY:
            print("⚠️  未設定 OPENAI_API_KEY，使用規則式判斷")
            return None
        
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = create_emotion_prompt(text)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一個語氣判斷專家，專門為文字添加 ElevenLabs 語氣標籤。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        result = response.choices[0].message.content.strip()
        return result
        
    except ImportError:
        print("⚠️  未安裝 openai 套件，請執行：pip install openai")
        return None
    except Exception as e:
        print(f"❌ OpenAI API 錯誤：{str(e)}")
        return None


def llm_emotion_route_anthropic(text: str, model: str = "claude-3-haiku-20240307") -> Optional[str]:
    """
    使用 Anthropic Claude API 判斷語氣
    
    Args:
        text: 輸入文字
        model: 使用的模型
        
    Returns:
        加上語氣標籤的文字，失敗返回 None
    """
    try:
        import anthropic
        
        if not ANTHROPIC_API_KEY:
            print("⚠️  未設定 ANTHROPIC_API_KEY，使用規則式判斷")
            return None
        
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        prompt = create_emotion_prompt(text)
        
        message = client.messages.create(
            model=model,
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        result = message.content[0].text.strip()
        return result
        
    except ImportError:
        print("⚠️  未安裝 anthropic 套件，請執行：pip install anthropic")
        return None
    except Exception as e:
        print(f"❌ Anthropic API 錯誤：{str(e)}")
        return None


def llm_emotion_route(
    text: str,
    provider: str = "openai",
    model: Optional[str] = None,
    fallback_to_rule: bool = True
) -> str:
    """
    主要接口：使用 LLM 判斷語氣並插入標籤
    
    Args:
        text: 輸入文字
        provider: LLM 提供者（"openai" 或 "anthropic"）
        model: 模型名稱（可選，使用環境變數或預設值）
        fallback_to_rule: 如果 LLM 失敗，是否回退到規則式判斷
        
    Returns:
        加上語氣標籤的文字
    """
    # 嘗試使用 LLM
    result = None
    
    if provider.lower() == "openai":
        model = model or OPENAI_MODEL  # 使用環境變數或提供的模型
        result = llm_emotion_route_openai(text, model)
    elif provider.lower() == "anthropic":
        model = model or "claude-3-haiku-20240307"
        result = llm_emotion_route_anthropic(text, model)
    else:
        print(f"⚠️  不支援的 provider: {provider}，使用規則式判斷")
    
    # 如果 LLM 失敗且允許回退，使用規則式判斷
    if not result and fallback_to_rule:
        from emotion_tag_engine import insert_emotion_tags
        result = insert_emotion_tags(text)
        print("📌 使用規則式語氣判斷")
    
    return result or text


# 測試函數
if __name__ == "__main__":
    test_texts = [
        "你知道嗎？我真的好感動。",
        "太好了！我們成功了！",
        "這是個秘密，不要告訴別人。",
        "氣死我了！",
        "你好，我是黃蓉！",
    ]
    
    print("=" * 60)
    print("🧠 LLM 語氣判斷器測試")
    print("=" * 60)
    print()
    
    for text in test_texts:
        print(f"原始：{text}")
        
        # 嘗試使用 OpenAI（如果可用）
        result = llm_emotion_route(text, provider="openai", fallback_to_rule=True)
        print(f"結果：{result}")
        print()

