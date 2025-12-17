"""
🧪 測試工具：用於測試和調試語氣標籤與語音產生
"""

from emotion_tag_engine import insert_emotion_tags, AVAILABLE_EMOTION_TAGS
from eleven_tts import generate_speech, get_voice_info, list_available_voices


def test_emotion_tags():
    """測試語氣標籤插入功能"""
    print("=" * 60)
    print("🧪 測試語氣標籤插入功能")
    print("=" * 60)
    print()
    
    test_cases = [
        "你好，我是黃蓉！",
        "這是個秘密，不要告訴別人",
        "嗚嗚，我好難過",
        "氣死我了！",
        "你知道嗎？",
        "今天天氣真好",
    ]
    
    for text in test_cases:
        tagged = insert_emotion_tags(text)
        print(f"原始：{text}")
        print(f"標籤：{tagged}")
        print()


def test_voice_info():
    """測試取得聲線資訊"""
    print("=" * 60)
    print("🔍 檢查聲線設定")
    print("=" * 60)
    print()
    
    voice_info = get_voice_info()
    if voice_info:
        print("✅ 聲線資訊：")
        print(f"  名稱：{voice_info.get('name', 'N/A')}")
        print(f"  Voice ID：{voice_info.get('voice_id', 'N/A')}")
        print(f"  類別：{voice_info.get('category', 'N/A')}")
    else:
        print("❌ 無法取得聲線資訊，請檢查 .env 設定")


def test_list_voices():
    """列出所有可用的聲線"""
    print("=" * 60)
    print("📋 列出所有可用聲線")
    print("=" * 60)
    print()
    
    voices = list_available_voices()
    if voices:
        print(f"找到 {len(voices)} 個聲線：\n")
        for i, voice in enumerate(voices, 1):
            print(f"{i}. {voice.get('name', 'N/A')}")
            print(f"   ID: {voice.get('voice_id', 'N/A')}")
            print(f"   類別: {voice.get('category', 'N/A')}")
            print()
    else:
        print("❌ 無法取得聲線列表，請檢查 API Key")


def test_single_speech(text: str = "你好，我是黃蓉"):
    """測試單一語音產生"""
    print("=" * 60)
    print("🎤 測試語音產生")
    print("=" * 60)
    print()
    
    tagged_text = insert_emotion_tags(text)
    print(f"原始文字：{text}")
    print(f"標籤文字：{tagged_text}")
    print()
    
    filename = "test_output.mp3"
    success = generate_speech(tagged_text, filename=filename)
    
    if success:
        print(f"\n✅ 測試成功！檔案：{filename}")
    else:
        print("\n❌ 測試失敗，請檢查設定")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "emotion":
            test_emotion_tags()
        elif command == "voice":
            test_voice_info()
        elif command == "list":
            test_list_voices()
        elif command == "speech":
            text = sys.argv[2] if len(sys.argv) > 2 else "你好，我是黃蓉"
            test_single_speech(text)
        else:
            print("可用指令：")
            print("  python test_tools.py emotion  - 測試語氣標籤")
            print("  python test_tools.py voice    - 檢查聲線設定")
            print("  python test_tools.py list     - 列出所有聲線")
            print("  python test_tools.py speech [文字] - 測試語音產生")
    else:
        # 執行所有測試
        test_emotion_tags()
        print("\n")
        test_voice_info()
        print("\n")
        test_single_speech()


