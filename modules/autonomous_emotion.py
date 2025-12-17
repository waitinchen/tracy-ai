"""
🧠 小軟自主語氣判斷系統

讓小軟能夠自主判斷何時該使用語氣標籤，並自由發揮表達方式。
"""

import random
import re
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from collections import deque

# 可用的語氣標籤
AVAILABLE_EMOTION_TAGS = [
    "excited", "whispers", "sarcastic", "curious", "softly", "crying",
    "starts laughing", "sings", "angry", "playful", "speaks quickly",
    "sighs", "happy", "sad", "surprised", "whispering", "echoes",
]


class AutonomousEmotionAgent:
    """
    自主語氣判斷代理
    
    讓小軟能夠：
    1. 自主判斷何時使用語氣標籤
    2. 根據對話上下文決定表達方式
    3. 有一定的隨機性和自主性
    4. 學習對話模式
    5. 保持情感持續性（情緒慣性曲線）
    """
    
    def __init__(self, autonomy_level: float = 0.7, emotion_persistence: float = 0.6):
        """
        初始化自主代理
        
        Args:
            autonomy_level: 自主程度（0.0-1.0），越高越自主
            emotion_persistence: 情感持續性（0.0-1.0），越高越容易保持相同情緒
        """
        self.autonomy_level = autonomy_level
        self.emotion_persistence = emotion_persistence  # 情感持續性參數
        self.conversation_history = deque(maxlen=20)  # 保留最近20條對話
        self.emotion_patterns = {}  # 學習的情緒模式
        self.last_emotion_time = {}  # 記錄上次使用某種情緒的時間
        self.current_emotion_state = None  # 當前情緒狀態
        self.emotion_momentum = {}  # 情緒動量（慣性）
        
        # 自主決策參數
        self.base_emotion_probability = 0.6  # 基礎使用語氣的概率
        self.context_weight = 0.3  # 上下文權重
        self.randomness_weight = 0.2  # 隨機性權重
        
    def should_use_emotion(self, text: str) -> bool:
        """
        判斷是否應該使用語氣標籤
        
        Args:
            text: 輸入文字
            
        Returns:
            是否應該使用語氣標籤
        """
        # 1. 基礎判斷：文字長度和內容
        text_length = len(text)
        if text_length < 3:
            return False  # 太短的文字不需要語氣
        
        # 2. 檢查是否有明顯的情緒關鍵字
        strong_emotion_keywords = [
            "哭", "難過", "開心", "生氣", "驚訝", "秘密", 
            "感動", "氣死", "太好了", "你知道嗎"
        ]
        has_strong_emotion = any(keyword in text for keyword in strong_emotion_keywords)
        
        if has_strong_emotion:
            return True  # 有強烈情緒，應該使用語氣
        
        # 3. 檢查對話上下文
        recent_emotion_count = self._count_recent_emotions()
        if recent_emotion_count > 3:
            # 最近使用太多語氣，這次可能不需要
            return random.random() < (0.5 * self.autonomy_level)
        
        # 4. 自主決策：根據自主程度決定
        base_prob = self.base_emotion_probability * self.autonomy_level
        
        # 根據文字特徵調整概率
        if "？" in text or "?" in text:
            base_prob += 0.2  # 疑問句更可能需要語氣
        if "！" in text or "!" in text:
            base_prob += 0.3  # 感嘆句更可能需要語氣
        
        # 隨機性：讓小軟有自主性
        randomness = random.random() * self.randomness_weight
        
        final_probability = min(base_prob + randomness, 0.95)
        
        return random.random() < final_probability
    
    def choose_emotion_tags(self, text: str, use_llm: bool = True) -> Optional[List[str]]:
        """
        自主選擇語氣標籤
        
        Args:
            text: 輸入文字
            use_llm: 是否使用 LLM 輔助判斷
            
        Returns:
            選擇的語氣標籤列表，如果不需要則返回 None
        """
        # 1. 判斷是否需要語氣
        if not self.should_use_emotion(text):
            return None  # 不需要語氣，返回原始文字
        
        # 2. 使用 LLM 判斷（如果可用）
        if use_llm:
            try:
                from modules.llm_emotion_router import llm_emotion_route_openai
                llm_result = llm_emotion_route_openai(text)
                if llm_result and llm_result != text:
                    # 從 LLM 結果中提取標籤
                    tags = self._extract_tags_from_text(llm_result)
                    if tags:
                        self._record_emotion_usage(tags, text)
                        return tags
            except:
                pass  # LLM 失敗，使用自主判斷
        
        # 3. 自主判斷（基於規則和上下文）
        tags = self._autonomous_emotion_selection(text)
        
        if tags:
            self._record_emotion_usage(tags, text)
        
        return tags
    
    def _autonomous_emotion_selection(self, text: str) -> List[str]:
        """
        自主選擇語氣標籤（不使用 LLM）
        
        Args:
            text: 輸入文字
            
        Returns:
            語氣標籤列表
        """
        text_lower = text.lower()
        selected_tags = []
        
        # 根據關鍵字判斷
        emotion_rules = {
            "excited": ["你好", "哈囉", "太好了", "真棒", "成功"],
            "whispers": ["秘密", "悄悄話", "偷偷", "不要告訴"],
            "crying": ["哭", "難過", "傷心", "感動", "眼淚"],
            "softly": ["溫柔", "輕柔", "輕輕"],
            "angry": ["氣死", "生氣", "憤怒", "討厭"],
            "curious": ["你知道嗎", "為什麼", "怎麼", "什麼"],
            "playful": ["調皮", "好玩", "有趣"],
            "happy": ["開心", "高興", "快樂"],
            "sad": ["難過", "悲傷", "傷心"],
            "surprised": ["驚訝", "驚奇", "沒想到"],
            "sighs": ["嘆氣", "無奈"],
        }
        
        # 匹配關鍵字
        for tag, keywords in emotion_rules.items():
            if any(keyword in text_lower for keyword in keywords):
                selected_tags.append(tag)
        
        # 如果沒有匹配到，根據上下文和隨機性決定
        if not selected_tags:
            # 檢查對話歷史，看最近使用的情緒
            recent_tags = self._get_recent_emotion_tags()
            
            # 情感持續性：根據動量決定是否延續情緒
            if self.current_emotion_state and self.emotion_persistence > 0:
                momentum = self._get_emotion_momentum(self.current_emotion_state)
                persistence_prob = self.emotion_persistence * momentum
                
                if random.random() < persistence_prob:
                    # 延續當前情緒
                    selected_tags.append(self.current_emotion_state)
                elif recent_tags:
                    # 有時延續相同情緒
                    if random.random() < 0.3:
                        selected_tags.append(random.choice(recent_tags))
                    else:
                        # 有時改變情緒
                        selected_tags.append(random.choice(["playful", "happy", "curious"]))
                else:
                    # 首次對話，使用黃蓉的典型風格
                    if random.random() < 0.6:
                        selected_tags.append("playful")
                    if random.random() < 0.4:
                        selected_tags.append("speaks quickly")
            else:
                # 沒有持續性要求，使用原有邏輯
                if recent_tags:
                    # 有時延續相同情緒
                    if random.random() < 0.3:
                        selected_tags.append(random.choice(recent_tags))
                    else:
                        # 有時改變情緒
                        selected_tags.append(random.choice(["playful", "happy", "curious"]))
                else:
                    # 首次對話，使用黃蓉的典型風格
                    if random.random() < 0.6:
                        selected_tags.append("playful")
                    if random.random() < 0.4:
                        selected_tags.append("speaks quickly")
        
        # 去重並限制數量
        selected_tags = list(set(selected_tags))[:2]  # 最多2個標籤
        
        return selected_tags if selected_tags else None
    
    def _extract_tags_from_text(self, text: str) -> List[str]:
        """
        從文字中提取語氣標籤
        
        Args:
            text: 包含標籤的文字，例如 "[playful] 你好"
            
        Returns:
            標籤列表
        """
        tags = []
        pattern = r'\[([^\]]+)\]'
        matches = re.findall(pattern, text)
        
        for match in matches:
            if match in AVAILABLE_EMOTION_TAGS:
                tags.append(match)
        
        return tags
    
    def _count_recent_emotions(self, window: int = 5) -> int:
        """
        計算最近使用語氣的次數
        
        Args:
            window: 檢查的對話數量
            
        Returns:
            使用語氣的次數
        """
        count = 0
        for entry in list(self.conversation_history)[-window:]:
            if entry.get('has_emotion', False):
                count += 1
        return count
    
    def _get_recent_emotion_tags(self, window: int = 5) -> List[str]:
        """
        獲取最近使用的語氣標籤
        
        Args:
            window: 檢查的對話數量
            
        Returns:
            標籤列表
        """
        tags = []
        for entry in list(self.conversation_history)[-window:]:
            if entry.get('emotion_tags'):
                tags.extend(entry['emotion_tags'])
        return tags
    
    def _get_emotion_momentum(self, tag: str) -> float:
        """
        獲取情緒動量（慣性）
        
        Args:
            tag: 情緒標籤
            
        Returns:
            動量值（0.0-1.0），越高表示越容易延續該情緒
        """
        if tag not in self.emotion_momentum:
            return 0.0
        
        # 計算時間衰減（最近使用的情緒動量更高）
        momentum = self.emotion_momentum[tag]
        
        # 如果最近使用過，增加動量
        if tag in self.last_emotion_time:
            time_since = (datetime.now() - self.last_emotion_time[tag]).total_seconds()
            # 30秒內使用過，動量不衰減；超過30秒開始衰減
            if time_since < 30:
                momentum = min(1.0, momentum + 0.2)
            else:
                # 指數衰減
                decay_factor = max(0.0, 1.0 - (time_since - 30) / 300)  # 5分鐘內完全衰減
                momentum *= decay_factor
        
        return max(0.0, min(1.0, momentum))
    
    def _update_emotion_momentum(self, tags: List[str]):
        """
        更新情緒動量
        
        Args:
            tags: 使用的情緒標籤列表
        """
        for tag in tags:
            if tag not in self.emotion_momentum:
                self.emotion_momentum[tag] = 0.0
            
            # 增加該情緒的動量
            self.emotion_momentum[tag] = min(1.0, self.emotion_momentum[tag] + 0.3)
            
            # 其他情緒動量衰減
            for other_tag in self.emotion_momentum:
                if other_tag != tag:
                    self.emotion_momentum[other_tag] *= 0.8  # 衰減20%
        
        # 更新當前情緒狀態
        if tags:
            self.current_emotion_state = tags[0]  # 使用第一個標籤作為主要情緒
        else:
            # 如果沒有標籤，當前情緒狀態逐漸衰減
            if self.current_emotion_state:
                self.emotion_momentum[self.current_emotion_state] *= 0.9
    
    def _record_emotion_usage(self, tags: List[str], text: str):
        """
        記錄語氣使用情況
        
        Args:
            tags: 使用的標籤
            text: 文字內容
        """
        self.conversation_history.append({
            'text': text,
            'emotion_tags': tags,
            'has_emotion': True,
            'timestamp': datetime.now()
        })
        
        # 更新情緒模式
        for tag in tags:
            if tag not in self.emotion_patterns:
                self.emotion_patterns[tag] = 0
            self.emotion_patterns[tag] += 1
            self.last_emotion_time[tag] = datetime.now()
        
        # 更新情緒動量（情感持續性）
        self._update_emotion_momentum(tags)
    
    def process_text(self, text: str, use_llm: bool = True) -> str:
        """
        處理文字，自主決定是否添加語氣標籤
        
        Args:
            text: 輸入文字
            use_llm: 是否使用 LLM 輔助
            
        Returns:
            處理後的文字（可能包含語氣標籤）
        """
        # 記錄對話（無論是否使用語氣）
        self.conversation_history.append({
            'text': text,
            'emotion_tags': None,
            'has_emotion': False,
            'timestamp': datetime.now()
        })
        
        # 自主選擇語氣標籤
        tags = self.choose_emotion_tags(text, use_llm=use_llm)
        
        # 如果沒有使用語氣，也更新動量（逐漸衰減）
        if not tags:
            if self.current_emotion_state:
                self.emotion_momentum[self.current_emotion_state] *= 0.95  # 輕微衰減
        
        if tags:
            # 添加標籤
            tag_string = ''.join([f'[{tag}]' for tag in tags])
            return f"{tag_string} {text}"
        else:
            # 不使用語氣標籤，返回原始文字
            return text
    
    def get_autonomy_stats(self) -> Dict:
        """
        獲取自主決策統計
        
        Returns:
            統計資訊
        """
        total_messages = len(self.conversation_history)
        emotion_messages = sum(1 for e in self.conversation_history if e.get('has_emotion'))
        
        return {
            'total_messages': total_messages,
            'emotion_messages': emotion_messages,
            'emotion_usage_rate': emotion_messages / total_messages if total_messages > 0 else 0,
            'autonomy_level': self.autonomy_level,
            'emotion_persistence': self.emotion_persistence,
            'emotion_patterns': dict(self.emotion_patterns),
            'current_emotion_state': self.current_emotion_state,
            'emotion_momentum': dict(self.emotion_momentum)
        }


def autonomous_emotion_route(
    text: str,
    autonomy_level: float = 0.7,
    use_llm: bool = True,
    agent: Optional[AutonomousEmotionAgent] = None
) -> str:
    """
    自主語氣路由（主要接口）
    
    Args:
        text: 輸入文字
        autonomy_level: 自主程度（0.0-1.0）
        use_llm: 是否使用 LLM 輔助
        agent: 可選的代理實例（用於保持對話上下文）
        
    Returns:
        處理後的文字
    """
    if agent is None:
        agent = AutonomousEmotionAgent(autonomy_level=autonomy_level)
    
    return agent.process_text(text, use_llm=use_llm)


# 全域代理實例（用於保持對話上下文）
_global_agent = None

def get_global_agent(autonomy_level: float = 0.7, emotion_persistence: float = 0.6) -> AutonomousEmotionAgent:
    """
    獲取全域代理實例（保持對話上下文）
    
    Args:
        autonomy_level: 自主程度
        emotion_persistence: 情感持續性
        
    Returns:
        代理實例
    """
    global _global_agent
    if _global_agent is None:
        _global_agent = AutonomousEmotionAgent(autonomy_level=autonomy_level, emotion_persistence=emotion_persistence)
    return _global_agent


# 測試函數
if __name__ == "__main__":
    print("=" * 60)
    print("🧠 小軟自主語氣判斷系統測試")
    print("=" * 60)
    print()
    
    agent = AutonomousEmotionAgent(autonomy_level=0.7)
    
    test_texts = [
        "你好",
        "這是個秘密",
        "你知道嗎？我真的好感動。",
        "太好了！",
        "今天天氣不錯",
        "氣死我了！",
    ]
    
    for text in test_texts:
        result = agent.process_text(text, use_llm=False)
        tags = agent.choose_emotion_tags(text, use_llm=False)
        
        print(f"原文：{text}")
        print(f"標籤：{tags}")
        print(f"結果：{result}")
        print()
    
    # 顯示統計
    stats = agent.get_autonomy_stats()
    print("=" * 60)
    print("📊 自主決策統計")
    print("=" * 60)
    print(f"總訊息數：{stats['total_messages']}")
    print(f"使用語氣數：{stats['emotion_messages']}")
    print(f"語氣使用率：{stats['emotion_usage_rate']:.2%}")
    print(f"自主程度：{stats['autonomy_level']:.2%}")
    print(f"情緒模式：{stats['emotion_patterns']}")

