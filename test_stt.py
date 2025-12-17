"""
🎙️ 語音輸入測試（使用 OpenAI Whisper API）

需要先錄製音訊檔案，然後轉換為文字
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(audio_file):
    """
    使用 OpenAI Whisper API 轉換語音為文字
    
    Args:
        audio_file: 音訊檔案路徑
    
    Returns:
        轉換後的文字
    """
    if not os.path.exists(audio_file):
        print(f"❌ 檔案不存在: {audio_file}")
        return None
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 未設定 OPENAI_API_KEY")
        return None
    
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        print(f"🔄 正在轉換語音: {audio_file}")
        
        with open(audio_file, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="zh"
            )
        
        text = transcript.text
        print(f"✅ 轉換完成: {text}")
        return text
        
    except ImportError:
        print("❌ 未安裝 openai 套件，請執行: pip install openai")
        return None
    except Exception as e:
        print(f"❌ 轉換失敗: {str(e)}")
        return None


def record_audio_windows():
    """
    Windows 錄音提示
    
    Returns:
        錄製的檔案路徑
    """
    print("=" * 60)
    print("🎙️  語音錄製提示")
    print("=" * 60)
    print("\n請使用以下方式錄製語音：")
    print("1. 使用 Windows 語音錄音機")
    print("2. 使用 Audacity")
    print("3. 使用其他錄音軟體")
    print("\n錄製完成後，請輸入檔案路徑")
    print("支援格式: .mp3, .wav, .m4a, .webm\n")
    
    audio_file = input("請輸入音訊檔案路徑: ").strip().strip('"')
    
    if os.path.exists(audio_file):
        return audio_file
    else:
        print(f"❌ 檔案不存在: {audio_file}")
        return None


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description="語音轉文字測試")
    parser.add_argument(
        "audio_file",
        nargs="?",
        help="音訊檔案路徑（如果未提供，會提示錄音）"
    )
    
    args = parser.parse_args()
    
    if args.audio_file:
        audio_file = args.audio_file
    else:
        audio_file = record_audio_windows()
    
    if audio_file:
        text = transcribe_audio(audio_file)
        if text:
            print(f"\n📝 轉換結果: {text}")
            
            # 可以選擇繼續處理
            continue_process = input("\n是否繼續處理（加上語氣標籤並產生語音）? (y/n): ").strip().lower()
            if continue_process == 'y':
                from modules.llm_emotion_router import llm_emotion_route
                from eleven_tts import generate_speech
                
                tagged_text = llm_emotion_route(text, provider="openai", fallback_to_rule=True)
                print(f"🏷️  標籤後: {tagged_text}")
                
                output_file = "stt_output.mp3"
                if generate_speech(tagged_text, filename=output_file):
                    print(f"✅ 語音已產生: {output_file}")
                    import os
                    os.startfile(output_file)


if __name__ == "__main__":
    main()


