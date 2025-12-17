"""
🎤 本地端雙向語音對話測試系統

功能：
1. 語音輸入（STT - Speech to Text）
2. 文字處理（語氣判斷）
3. 語音輸出（TTS - Text to Speech）
4. 循環對話
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

# 導入模組
from emotion_tag_engine import insert_emotion_tags
from modules.llm_emotion_router import llm_emotion_route
from eleven_tts import generate_speech


class VoiceConversation:
    """語音對話系統"""
    
    def __init__(self, use_llm=True, provider="openai"):
        self.use_llm = use_llm
        self.provider = provider
        self.conversation_history = []
        
    def speech_to_text(self, audio_file=None):
        """
        語音轉文字（STT）
        
        Args:
            audio_file: 音訊檔案路徑（如果為 None，則使用麥克風錄音）
        
        Returns:
            轉換後的文字
        """
        # 方法 1: 使用 OpenAI Whisper API
        if os.getenv("OPENAI_API_KEY"):
            try:
                import openai
                client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                
                if audio_file:
                    # 從檔案讀取
                    with open(audio_file, "rb") as f:
                        transcript = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=f,
                            language="zh"
                        )
                else:
                    # 從麥克風錄音（需要先錄製）
                    print("⚠️  請先錄製音訊檔案，或使用 audio_file 參數")
                    return None
                
                return transcript.text
            except ImportError:
                print("⚠️  未安裝 openai 套件")
            except Exception as e:
                print(f"❌ Whisper API 錯誤: {str(e)}")
        
        # 方法 2: 使用本地 Whisper（如果安裝）
        try:
            import whisper
            model = whisper.load_model("base")
            
            if audio_file:
                result = model.transcribe(audio_file, language="zh")
                return result["text"]
            else:
                print("⚠️  請先錄製音訊檔案")
                return None
        except ImportError:
            print("⚠️  未安裝 whisper 套件，請執行: pip install openai-whisper")
        except Exception as e:
            print(f"❌ Whisper 錯誤: {str(e)}")
        
        # 方法 3: 手動輸入（備用）
        print("⚠️  使用手動輸入模式（備用）")
        return input("請輸入文字: ").strip()
    
    def process_text(self, text):
        """
        處理文字（語氣判斷）
        
        Args:
            text: 輸入文字
        
        Returns:
            加上語氣標籤的文字
        """
        if self.use_llm and os.getenv("OPENAI_API_KEY"):
            try:
                tagged_text = llm_emotion_route(
                    text,
                    provider=self.provider,
                    fallback_to_rule=True
                )
                return tagged_text
            except Exception as e:
                print(f"⚠️  LLM 判斷失敗，使用規則式: {str(e)}")
                return insert_emotion_tags(text)
        else:
            return insert_emotion_tags(text)
    
    def text_to_speech(self, text, output_file=None):
        """
        文字轉語音（TTS）
        
        Args:
            text: 要轉換的文字
            output_file: 輸出檔案名稱
        
        Returns:
            音訊檔案路徑
        """
        if not output_file:
            timestamp = int(time.time())
            output_file = f"conversation_output_{timestamp}.mp3"
        
        success = generate_speech(text, filename=output_file)
        
        if success:
            return output_file
        else:
            return None
    
    def play_audio(self, audio_file):
        """
        播放音訊檔案
        
        Args:
            audio_file: 音訊檔案路徑
        """
        try:
            # 方法 1: 使用 playsound
            try:
                from playsound import playsound
                playsound(audio_file)
                return True
            except ImportError:
                pass
            
            # 方法 2: 使用 pydub
            try:
                from pydub import AudioSegment
                from pydub.playback import play
                audio = AudioSegment.from_mp3(audio_file)
                play(audio)
                return True
            except ImportError:
                pass
            
            # 方法 3: Windows 系統命令
            if sys.platform == 'win32':
                os.startfile(audio_file)
                return True
            
            # 方法 4: 提示手動播放
            print(f"💡 請手動播放音訊檔案: {audio_file}")
            return False
            
        except Exception as e:
            print(f"❌ 播放錯誤: {str(e)}")
            print(f"💡 請手動播放: {audio_file}")
            return False
    
    def conversation_loop(self, input_mode="manual"):
        """
        對話循環
        
        Args:
            input_mode: 輸入模式 ("manual" 或 "voice")
        """
        print("=" * 60)
        print("🎤 黃蓉語音對話系統")
        print("=" * 60)
        print("\n對話模式已啟動")
        print("輸入 'quit' 或 'exit' 結束對話\n")
        
        while True:
            try:
                # Step 1: 語音輸入或文字輸入
                if input_mode == "voice":
                    print("🎤 請說話（錄音中...）")
                    user_input = self.speech_to_text()
                    if not user_input:
                        print("⚠️  無法取得語音輸入，請使用手動輸入模式")
                        user_input = input("📝 請輸入文字: ").strip()
                else:
                    user_input = input("📝 請輸入文字: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', '退出', '結束']:
                    print("\n👋 對話結束，再見！")
                    break
                
                # 記錄對話歷史
                self.conversation_history.append({"role": "user", "text": user_input})
                print(f"\n👤 你說: {user_input}")
                
                # Step 2: 處理文字（語氣判斷）
                print("🔄 處理中...")
                tagged_text = self.process_text(user_input)
                print(f"🏷️  標籤後: {tagged_text}")
                
                # Step 3: 產生語音
                print("🎵 產生語音中...")
                audio_file = self.text_to_speech(tagged_text)
                
                if audio_file:
                    print(f"✅ 語音已產生: {audio_file}")
                    
                    # Step 4: 播放語音
                    print("🔊 播放語音...")
                    self.play_audio(audio_file)
                    
                    # 記錄對話歷史
                    self.conversation_history.append({
                        "role": "assistant",
                        "text": tagged_text,
                        "audio": audio_file
                    })
                else:
                    print("❌ 語音產生失敗")
                
                print("\n" + "-" * 60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 對話中斷，再見！")
                break
            except Exception as e:
                print(f"\n❌ 發生錯誤: {str(e)}")
                import traceback
                traceback.print_exc()
                print()


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description="黃蓉語音對話系統")
    parser.add_argument(
        "--mode",
        choices=["manual", "voice"],
        default="manual",
        help="輸入模式: manual (手動輸入) 或 voice (語音輸入)"
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="不使用 LLM 語氣判斷，使用規則式判斷"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic"],
        default="openai",
        help="LLM 提供者"
    )
    
    args = parser.parse_args()
    
    # 創建對話系統
    conversation = VoiceConversation(
        use_llm=not args.no_llm,
        provider=args.provider
    )
    
    # 啟動對話循環
    conversation.conversation_loop(input_mode=args.mode)


if __name__ == "__main__":
    main()


