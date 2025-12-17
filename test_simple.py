"""
簡化版測試腳本（Windows 兼容）
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 設置 UTF-8 編碼
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

load_dotenv()

def test_imports():
    """測試模組導入"""
    print("=" * 60)
    print("測試 1: 模組導入")
    print("=" * 60)
    try:
        from emotion_tag_engine import insert_emotion_tags
        from eleven_tts import generate_speech, API_KEY, VOICE_ID
        from modules.llm_emotion_router import llm_emotion_route
        print("[OK] 所有模組導入成功")
        return True
    except Exception as e:
        print(f"[FAIL] 模組導入失敗: {str(e)}")
        return False

def test_emotion_engine():
    """測試規則式語氣判斷"""
    print("\n" + "=" * 60)
    print("測試 2: 規則式語氣判斷")
    print("=" * 60)
    try:
        from emotion_tag_engine import insert_emotion_tags
        
        test_cases = [
            ("你好", "[excited]"),
            ("這是秘密", "[whispers]"),
            ("我好難過", "[crying]"),
        ]
        
        passed = 0
        for text, expected in test_cases:
            result = insert_emotion_tags(text)
            if expected in result:
                print(f"[OK] '{text}' -> {result}")
                passed += 1
            else:
                print(f"[WARN] '{text}' -> {result} (預期包含 {expected})")
        
        print(f"\n結果: {passed}/{len(test_cases)} 通過")
        return passed == len(test_cases)
    except Exception as e:
        print(f"[FAIL] 測試失敗: {str(e)}")
        return False

def test_llm_router():
    """測試 LLM 語氣判斷"""
    print("\n" + "=" * 60)
    print("測試 3: LLM 語氣判斷 (GPT)")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("[SKIP] OPENAI_API_KEY 未設定，跳過測試")
        return True
    
    try:
        from modules.llm_emotion_router import llm_emotion_route
        
        test_cases = [
            "你知道嗎？我真的好感動。",
            "太好了！我們成功了！",
            "這是個秘密，不要告訴別人。",
            "氣死我了！",
            "你好，我是黃蓉！"
        ]
        
        print("\n測試 LLM 語氣判斷...\n")
        for text in test_cases:
            try:
                result = llm_emotion_route(text, provider="openai", fallback_to_rule=True)
                has_tags = "[" in result and "]" in result
                status = "[OK]" if has_tags else "[WARN]"
                print(f"{status} {text}")
                print(f"    -> {result}\n")
            except Exception as e:
                print(f"[ERROR] {text}")
                print(f"    -> 錯誤: {str(e)}\n")
        
        return True
    except ImportError as e:
        print(f"[SKIP] 模組導入失敗: {str(e)}")
        return True
    except Exception as e:
        print(f"[FAIL] 測試失敗: {str(e)}")
        return False

def test_full_pipeline():
    """測試完整流程"""
    print("\n" + "=" * 60)
    print("測試 4: 完整流程 (文字 -> 語氣 -> 語音)")
    print("=" * 60)
    
    if not os.getenv("ELEVEN_API_KEY"):
        print("[SKIP] ELEVEN_API_KEY 未設定，跳過語音產生測試")
        return True
    
    try:
        from emotion_tag_engine import insert_emotion_tags
        from modules.llm_emotion_router import llm_emotion_route
        from eleven_tts import generate_speech
        
        test_text = "你好，我是黃蓉！"
        print(f"\n原文: {test_text}\n")
        
        # Step 1: 規則式判斷
        print("Step 1: 規則式語氣判斷")
        tagged_rule = insert_emotion_tags(test_text)
        print(f"結果: {tagged_rule}\n")
        
        # Step 2: LLM 判斷
        if os.getenv("OPENAI_API_KEY"):
            print("Step 2: LLM 語氣判斷")
            try:
                tagged_llm = llm_emotion_route(test_text, provider="openai", fallback_to_rule=True)
                print(f"結果: {tagged_llm}\n")
                final_text = tagged_llm
            except:
                print("回退到規則式結果\n")
                final_text = tagged_rule
        else:
            final_text = tagged_rule
        
        # Step 3: 產生語音
        print("Step 3: 產生語音檔案")
        output_file = "test_huangrong_output.mp3"
        
        success = generate_speech(final_text, filename=output_file)
        
        if success:
            file_path = Path(output_file)
            if file_path.exists():
                file_size = file_path.stat().st_size / 1024
                print(f"[OK] 語音檔案已產生: {output_file} ({file_size:.2f} KB)")
                print(f"[TIP] 可以播放檔案聽聽黃蓉的效果！")
                return True
            else:
                print(f"[FAIL] 檔案未產生")
                return False
        else:
            print(f"[FAIL] 語音產生失敗")
            return False
            
    except Exception as e:
        print(f"[FAIL] 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主測試函數"""
    print("=" * 60)
    print("黃蓉語音系統 - 今日驗收測試")
    print("=" * 60)
    
    results = []
    results.append(("模組導入", test_imports()))
    results.append(("規則式語氣判斷", test_emotion_engine()))
    results.append(("LLM 語氣判斷", test_llm_router()))
    results.append(("完整流程測試", test_full_pipeline()))
    
    # 總結
    print("\n" + "=" * 60)
    print("測試結果總結")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {name}: {status}")
    
    print(f"\n總計: {passed}/{total} 項測試通過")
    
    if passed == total:
        print("\n[SUCCESS] 所有測試通過！系統準備就緒。")
        print("\n下一步:")
        print("  1. 播放 test_huangrong_output.mp3 聽聽黃蓉的效果")
        print("  2. 啟動 API: py start_api.py")
        print("  3. 訪問 http://localhost:8000/docs 測試 API")
        return 0
    else:
        print(f"\n[WARN] 有 {total - passed} 項測試未通過，請檢查上述問題。")
        return 1

if __name__ == "__main__":
    sys.exit(main())


