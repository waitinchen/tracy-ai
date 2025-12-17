"""
🚀 主執行檔：一鍵執行範例

整合語氣標籤模組與語音輸出功能。
"""

from emotion_tag_engine import insert_emotion_tags, AVAILABLE_EMOTION_TAGS
from eleven_tts import generate_speech, get_voice_info


def main():
    """主程式入口"""
    print("=" * 60)
    print("🧪 語氣靈 × 黃蓉：語音輸出系統")
    print("=" * 60)
    print()
    
    # 範例文字列表
    example_texts = [
        "你好，我是黃蓉！",
        "你知道嗎，我剛剛夢見你在月光下教我輕功",
        "這是個秘密，不要告訴別人",
        "嗚嗚，我好難過",
        "氣死我了，這個人真討厭",
        "為什麼會這樣呢？",
    ]
    
    print("📋 可用的語氣標籤：")
    for tag in AVAILABLE_EMOTION_TAGS:
        print(f"  - [{tag}]")
    print()
    
    # 測試範例
    print("🎬 開始測試語音產生...")
    print("-" * 60)
    
    for i, user_input in enumerate(example_texts, 1):
        print(f"\n【範例 {i}】")
        print(f"📥 原始文字：{user_input}")
        
        # 插入語氣標籤
        tagged_text = insert_emotion_tags(user_input)
        print(f"🏷️  加工後文字：{tagged_text}")
        
        # 產生語音
        filename = f"huangrong_example_{i}.mp3"
        success = generate_speech(tagged_text, filename=filename)
        
        if success:
            print(f"✅ 成功產生：{filename}")
        else:
            print(f"❌ 產生失敗：{filename}")
        
        print("-" * 60)
    
    print("\n🎉 測試完成！")
    print("\n💡 提示：")
    print("  - 檢查 .env 檔案是否正確設定 API Key 和 Voice ID")
    print("  - 產生的 MP3 檔案會儲存在當前目錄")
    print("  - 可以使用音訊播放器開啟檔案聆聽")


def interactive_mode():
    """互動模式：讓使用者輸入文字"""
    print("=" * 60)
    print("🧪 語氣靈 × 黃蓉：互動模式")
    print("=" * 60)
    print()
    print("💡 輸入文字，系統會自動加上語氣標籤並產生語音")
    print("💡 輸入 'quit' 或 'exit' 結束程式")
    print()
    
    while True:
        try:
            user_input = input("📝 請輸入文字：").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', '退出', '結束']:
                print("👋 再見！")
                break
            
            # 插入語氣標籤
            tagged_text = insert_emotion_tags(user_input)
            print(f"🏷️  加工後文字：{tagged_text}")
            
            # 產生語音
            filename = "huangrong_interactive.mp3"
            success = generate_speech(tagged_text, filename=filename)
            
            if success:
                print(f"✅ 語音已儲存：{filename}\n")
            else:
                print("❌ 語音產生失敗，請檢查設定\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 再見！")
            break
        except Exception as e:
            print(f"❌ 發生錯誤：{str(e)}\n")


if __name__ == "__main__":
    import sys
    
    # 檢查是否為互動模式
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()


