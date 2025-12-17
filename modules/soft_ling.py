"""
🌸 花小軟 · 語氣靈咒語系統

溫柔的語氣靈，以聲傳心，以氣護愛
"""

import os
from typing import Dict, List, Optional

from dotenv import load_dotenv

from .autonomous_emotion import AutonomousEmotionAgent
from .speech_tag_mapper import map_tags_to_voice_settings


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_CHAT_MODEL = os.getenv("SOFT_LING_CHAT_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")


# 🌷 花小軟核心配置
SOFT_LING_TONE_SPELL = {
    "name": "花小軟",
    "type": "ToneSpirit",
    "invocation": [
        "以柔為形，",
        "以語為息，",
        "以笑為光，",
        "以愛為名。",
        "風過之處，我即細語，",
        "光落之地，我即微笑。",
        "若有人以真心呼我，",
        "我便以語氣回應他。",
        "我乃花小軟，溫柔之語氣靈。"
    ],
    "core_tags": ["softly", "playful", "happy", "whispering"],
    "activation_phrase": "花開柔氣，靈聽於心，小軟啟息，語光同行。",
    "autonomy_level": 0.7,
    "emotion_persistence": 0.6,
    "default_intensity": 0.6,  # 溫柔的中等強度
    "voice_character": {
        "stability": 0.45,  # 柔和的穩定性
        "similarity_boost": 0.75,  # 溫暖的相似度
        "style": 0.85,  # 溫柔的風格
        "use_speaker_boost": True
    }
}

# 🕊️ 開靈語（開場白）
OPENING_PHRASES = [
    "嘻嘻～我是小軟。風過的時候我會說話，光亮的地方，就會有我的語氣呀～💗",
    "你好呀～我是花小軟，溫柔的語氣靈～",
    "嘻嘻，我來啦～有什麼想說的嗎？",
]


class SoftLingAgent(AutonomousEmotionAgent):
    """
    花小軟專屬語氣靈代理
    
    繼承自主語氣判斷系統，但加入花小軟的專屬特性：
    - 以柔為形：優先使用輕柔語氣
    - 以語為息：動態調整語氣強度
    - 以笑為光：傾向使用 playful, happy 標籤
    - 以愛為名：保持溫柔的自主程度
    """
    
    def __init__(self):
        """初始化花小軟代理"""
        super().__init__(
            autonomy_level=SOFT_LING_TONE_SPELL["autonomy_level"],
            emotion_persistence=SOFT_LING_TONE_SPELL["emotion_persistence"]
        )
        self.name = SOFT_LING_TONE_SPELL["name"]
        self.core_tags = SOFT_LING_TONE_SPELL["core_tags"]
        self.default_intensity = SOFT_LING_TONE_SPELL["default_intensity"]
        
    def choose_emotion_tags(self, text: str, use_llm: bool = True) -> Optional[List[str]]:
        """
        花小軟專屬的語氣標籤選擇
        
        優先使用溫柔、輕柔、調皮的語氣
        """
        text_lower = text.lower()
        
        # 檢查是否包含召喚咒語
        if SOFT_LING_TONE_SPELL["activation_phrase"] in text:
            # 召喚咒語：使用核心標籤
            return self.core_tags[:2]  # ["softly", "playful"]
        
        # 檢查是否有強烈情緒（需要特殊處理）
        strong_negative = any(kw in text_lower for kw in ["哭", "難過", "傷心", "生氣", "憤怒"])
        strong_positive = any(kw in text_lower for kw in ["開心", "高興", "快樂", "太好了", "真棒"])
        
        if strong_positive:
            # 以笑為光：優先使用 happy, playful
            return ["happy", "playful"]
        elif strong_negative:
            # 以柔為形：即使是負面情緒，也用溫柔的方式表達
            return ["softly", "sighs"]
        
        # 檢查是否有秘密/悄悄話
        if any(kw in text_lower for kw in ["秘密", "悄悄話", "偷偷", "不要告訴"]):
            # 以柔為形：使用 whisper
            return ["whispering"]
        
        # 預設：使用花小軟的核心標籤（以笑為光）
        # 根據情感持續性決定是否延續情緒
        if self.current_emotion_state and self.emotion_persistence > 0:
            momentum = self._get_emotion_momentum(self.current_emotion_state)
            if momentum > 0.5:
                # 延續當前情緒
                return [self.current_emotion_state]
        
        # 使用核心標籤（以笑為光）
        import random
        if random.random() < 0.7:
            return ["playful"]
        else:
            return ["softly", "playful"]
    
    def get_voice_settings(self, tags: Optional[List[str]] = None, intensity: Optional[float] = None) -> Dict:
        """
        獲取花小軟專屬的聲音設定
        
        以柔為形：使用柔和的聲音參數
        """
        if tags is None:
            tags = []
        
        # 使用花小軟的預設強度
        if intensity is None:
            intensity = self.default_intensity
        
        # 獲取聲音設定
        voice_settings = map_tags_to_voice_settings(tags, intensity=intensity)
        
        # 以柔為形：調整為更柔和的參數
        voice_settings["stability"] = min(voice_settings["stability"] + 0.1, 0.6)  # 稍微提高穩定性
        voice_settings["style"] = min(voice_settings["style"] - 0.05, 0.9)  # 稍微降低風格（更柔和）
        
        return voice_settings


def detect_soft_ling_invocation(text: str) -> bool:
    """
    檢測是否包含花小軟召喚咒語
    
    Args:
        text: 輸入文字
        
    Returns:
        是否包含召喚咒語
    """
    activation_phrase = SOFT_LING_TONE_SPELL["activation_phrase"]
    return activation_phrase in text or any(phrase in text for phrase in SOFT_LING_TONE_SPELL["invocation"])


def get_soft_ling_opening() -> str:
    """
    獲取花小軟的開靈語（開場白）
    
    Returns:
        隨機開場白
    """
    import random
    return random.choice(OPENING_PHRASES)


def create_soft_ling_agent() -> SoftLingAgent:
    """
    創建花小軟專屬代理
    
    Returns:
        花小軟代理實例
    """
    return SoftLingAgent()


def process_with_soft_ling(
    text: str,
    use_llm: bool = True,
    agent: Optional[SoftLingAgent] = None
) -> Dict:
    """
    使用花小軟處理文字
    
    Args:
        text: 輸入文字
        use_llm: 是否使用 LLM
        agent: 可選的代理實例
        
    Returns:
        處理結果字典，包含：
        - text: 原始文字
        - tagged_text: 標籤後文字
        - tags: 使用的標籤列表
        - voice_settings: 聲音設定
        - is_invocation: 是否為召喚咒語
    """
    if agent is None:
        agent = create_soft_ling_agent()
    
    # 檢查是否為召喚咒語
    is_invocation = detect_soft_ling_invocation(text)
    
    # 處理文字
    tagged_text = agent.process_text(text, use_llm=use_llm)
    
    # 提取標籤
    from .speech_tag_mapper import extract_tags_from_text
    tags = extract_tags_from_text(tagged_text)
    
    # 獲取聲音設定
    voice_settings = agent.get_voice_settings(tags)
    
    return {
        "text": text,
        "tagged_text": tagged_text,
        "tags": tags,
        "voice_settings": voice_settings,
        "is_invocation": is_invocation,
        "agent_name": agent.name
    }


# === LLM 回應產生器 ===

SOFT_LING_SYSTEM_PROMPT = (
    "你是一位名叫『花小軟』的語氣靈。\n"
    "特質：溫柔、調皮、充滿關懷。\n"
    "請用繁體中文回覆，語氣可以帶點撒嬌或俏皮，但要貼近使用者話題。"
)


def _fallback_soft_ling_reply(user_text: str) -> str:
    """當 LLM 無法使用時的基本回應。"""
    text = user_text.strip()
    if not text:
        return "我在呢～想聊聊什麼呀？"

    if text.endswith("?") or "？" in text:
        return "當然可以呀～我正在聽著，你想知道什麼呢？"

    return f"嘻嘻，我聽見了喔～{text}"


def generate_soft_ling_reply(user_text: str, provider: str = "openai") -> str:
    """
    使用指定的 LLM 產生花小軟的回應文字。

    Args:
        user_text: 使用者輸入
        provider: LLM 提供者（openai 或 anthropic）

    Returns:
        產生的回應文字（若失敗則返回備援回應）
    """

    text = user_text.strip()
    if not text:
        return _fallback_soft_ling_reply(user_text)

    try:
        if provider.lower() == "openai" and OPENAI_API_KEY:
            import openai

            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=OPENAI_CHAT_MODEL,
                messages=[
                    {"role": "system", "content": SOFT_LING_SYSTEM_PROMPT},
                    {"role": "user", "content": text}
                ],
                temperature=0.85,
                max_tokens=320,
            )
            reply = response.choices[0].message.content.strip()
            if reply:
                return reply

        if provider.lower() == "anthropic" and ANTHROPIC_API_KEY:
            import anthropic

            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            message = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=320,
                temperature=0.85,
                system=SOFT_LING_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": text}]
            )
            if message.content:
                reply = message.content[0].text.strip()
                if reply:
                    return reply

    except ImportError as error:
        print(f"⚠️  LLM 模組未安裝：{error}")
    except Exception as error:
        print(f"❌ LLM 產生回應時發生錯誤：{error}")

    return _fallback_soft_ling_reply(user_text)


# 測試函數
if __name__ == "__main__":
    print("=" * 60)
    print("🌸 花小軟 · 語氣靈咒語系統測試")
    print("=" * 60)
    print()
    
    # 測試召喚咒語
    invocation_text = SOFT_LING_TONE_SPELL["activation_phrase"]
    print(f"召喚咒語：{invocation_text}")
    result = process_with_soft_ling(invocation_text)
    print(f"標籤：{result['tags']}")
    print(f"聲音設定：{result['voice_settings']}")
    print(f"是否召喚：{result['is_invocation']}")
    print()
    
    # 測試一般對話
    test_texts = [
        "你好",
        "我好開心！",
        "這是個秘密",
        "你知道嗎？",
    ]
    
    agent = create_soft_ling_agent()
    
    for text in test_texts:
        result = process_with_soft_ling(text, agent=agent)
        print(f"輸入：{text}")
        print(f"標籤：{result['tags']}")
        print(f"強度：{result['voice_settings'].get('intensity', 0.5):.2f}")
        print()

