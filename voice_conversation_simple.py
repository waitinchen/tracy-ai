"""
🎤 簡化版語音對話測試（快速測試用）

使用手動輸入模擬語音對話流程
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# 設置 UTF-8 編碼
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

load_dotenv()

from emotion_tag_engine import insert_emotion_tags
from modules.llm_emotion_router import llm_emotion_route
from eleven_tts import generate_speech


def play_audio_windows(audio_file):
    """Windows 播放音訊"""
    try:
        os.startfile(audio_file)
        return True
    except Exception as e:
        print(f"播放錯誤: {str(e)}")
        return False


def conversation_test():
    """對話測試"""
    print("=" * 60)
    print("黃蓉語音對話系統 - 測試模式")
    print("=" * 60)
    print("\n這是一個簡化的對話測試")
    print("輸入文字，系統會自動加上語氣標籤並產生語音")
    print("輸入 'quit' 結束\n")
    
    use_llm = bool(os.getenv("OPENAI_API_KEY"))
    if use_llm:
        print("✅ LLM 語氣判斷已啟用（使用 GPT）")
    else:
        print("⚠️  LLM 語氣判斷未啟用（使用規則式判斷）")
    
    print("\n" + "-" * 60 + "\n")
    
    conversation_count = 0
    
    while True:
        try:
            # 輸入文字
            user_input = input("📝 你說: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', '退出', '結束']:
                print("\n👋 對話結束！")
                break
            
            conversation_count += 1
            print(f"\n[對話 #{conversation_count}]")
            
            # 處理文字（語氣判斷）
            print("🔄 處理中...")
            if use_llm:
                try:
                    tagged_text = llm_emotion_route(
                        user_input,
                        provider="openai",
                        fallback_to_rule=True
                    )
                    print(f"🏷️  標籤後: {tagged_text}")
                except Exception as e:
                    print(f"⚠️  LLM 失敗，使用規則式: {str(e)}")
                    tagged_text = insert_emotion_tags(user_input)
                    print(f"🏷️  標籤後: {tagged_text}")
            else:
                tagged_text = insert_emotion_tags(user_input)
                print(f"🏷️  標籤後: {tagged_text}")
            
            # 產生語音
            print("🎵 產生語音中...")
            timestamp = int(time.time())
            audio_file = f"conversation_{timestamp}.mp3"
            
            success = generate_speech(tagged_text, filename=audio_file)
            
            if success:
                print(f"✅ 語音已產生: {audio_file}")
                
                # 播放語音
                print("🔊 播放語音...")
                if play_audio_windows(audio_file):
                    print("✅ 播放中...")
                else:
                    print(f"💡 請手動播放: {audio_file}")
            else:
                print("❌ 語音產生失敗")
            
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 對話中斷！")
            break
        except Exception as e:
            print(f"\n❌ 錯誤: {str(e)}")
            import traceback
            traceback.print_exc()
            print()


if __name__ == "__main__":
    conversation_test()


