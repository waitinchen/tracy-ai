"""
測試自主語氣判斷系統
"""

import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from modules.autonomous_emotion import AutonomousEmotionAgent

print("=" * 60)
print("自主語氣判斷系統測試")
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
print("自主決策統計")
print("=" * 60)
print(f"總訊息數：{stats['total_messages']}")
print(f"使用語氣數：{stats['emotion_messages']}")
print(f"語氣使用率：{stats['emotion_usage_rate']:.2%}")
print(f"自主程度：{stats['autonomy_level']:.2%}")
print(f"情緒模式：{stats['emotion_patterns']}")


