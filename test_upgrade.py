"""
測試升級功能
"""

import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("升級功能測試")
print("=" * 60)
print()

# 1. 測試語氣強度調節
print("1. 語氣強度調節測試")
print("-" * 60)
from modules.speech_tag_mapper import map_tags_to_voice_settings

tags = ["excited"]
for intensity in [0.3, 0.5, 0.7, 0.9]:
    settings = map_tags_to_voice_settings(tags, intensity=intensity)
    print(f"強度 {intensity:.1f}: intensity={settings.get('intensity', 0.5):.2f}")
print()

# 2. 測試多語模式
print("2. 多語模式測試")
print("-" * 60)
from modules.voice_engine import detect_language, get_model_id_for_language

test_texts = [
    ("你好", "zh"),
    ("Hello", "en"),
    ("こんにちは", "ja"),
]

for text, expected in test_texts:
    detected = detect_language(text)
    model = get_model_id_for_language(detected)
    print(f"文字: {text} -> 檢測: {detected} (預期: {expected}), 模型: {model}")
print()

# 3. 測試情感持續性
print("3. 情感持續性測試")
print("-" * 60)
from modules.autonomous_emotion import AutonomousEmotionAgent

agent = AutonomousEmotionAgent(emotion_persistence=0.7)
agent.process_text("我好開心！")
agent.process_text("今天天氣不錯")
stats = agent.get_autonomy_stats()
print(f"當前情緒狀態: {stats.get('current_emotion_state')}")
print(f"情緒動量: {stats.get('emotion_momentum', {})}")
print()

# 4. 測試即時串流模組
print("4. 即時串流模組測試")
print("-" * 60)
try:
    from modules.stream_tts import stream_speech
    print("✅ stream_tts 模組導入成功")
except ImportError as e:
    print(f"❌ 導入失敗: {e}")
print()

print("=" * 60)
print("所有測試完成")
print("=" * 60)


