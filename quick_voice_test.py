"""
快速測試腳本：雙向語音對話
"""

import os
import sys
import time
from dotenv import load_dotenv

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

load_dotenv()

from emotion_tag_engine import insert_emotion_tags
from modules.llm_emotion_router import llm_emotion_route
from eleven_tts import generate_speech


def main():
    print("=" * 60)
    print("黃蓉語音對話系統 - 快速測試")
    print("=" * 60)
    print("\n輸入文字，系統會自動處理並播放語音")
    print("輸入 'quit' 結束\n")
    
    count = 0
    
    while True:
        try:
            text = input("📝 你說: ").strip()
            
            if not text:
                continue
            
            if text.lower() in ['quit', 'exit', '退出']:
                print("\n👋 再見！")
                break
            
            count += 1
            print(f"\n[對話 #{count}]")
            
            # 語氣判斷
            if os.getenv("OPENAI_API_KEY"):
                try:
                    tagged = llm_emotion_route(text, provider="openai", fallback_to_rule=True)
                except:
                    tagged = insert_emotion_tags(text)
            else:
                tagged = insert_emotion_tags(text)
            
            print(f"🏷️  {tagged}")
            
            # 產生語音
            audio_file = f"conv_{int(time.time())}.mp3"
            if generate_speech(tagged, filename=audio_file):
                print(f"✅ {audio_file}")
                try:
                    os.startfile(audio_file)
                except:
                    print(f"💡 請播放: {audio_file}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 再見！")
            break
        except Exception as e:
            print(f"❌ 錯誤: {e}\n")


if __name__ == "__main__":
    main()


