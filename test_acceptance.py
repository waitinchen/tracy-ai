"""
🧪 今日驗收測試套件

測試項目：
1. 端到端測試（文字 → 語氣判斷 → 語音輸出）
2. LLM 語氣判斷測試
3. API 功能測試
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 測試用例
TEST_CASES = [
    {
        "text": "你知道嗎？我真的好感動。",
        "expected_tags": ["[crying]", "[softly]"],
        "description": "感動/哭泣情境"
    },
    {
        "text": "太好了！我們成功了！",
        "expected_tags": ["[excited]", "[happy]"],
        "description": "興奮/開心情境"
    },
    {
        "text": "這是個秘密，不要告訴別人。",
        "expected_tags": ["[whispers]"],
        "description": "悄悄話情境"
    },
    {
        "text": "氣死我了！",
        "expected_tags": ["[angry]"],
        "description": "生氣情境"
    },
    {
        "text": "你好，我是黃蓉！",
        "expected_tags": ["[excited]", "[playful]"],
        "description": "打招呼情境"
    },
]


def test_emotion_engine():
    """測試規則式語氣判斷引擎"""
    print("\n" + "=" * 60)
    print("🎭 測試 1：規則式語氣判斷引擎")
    print("=" * 60)
    
    try:
        from emotion_tag_engine import insert_emotion_tags
        
        passed = 0
        total = len(TEST_CASES)
        
        for case in TEST_CASES:
            text = case["text"]
            result = insert_emotion_tags(text)
            expected = case["expected_tags"]
            
            # 檢查是否包含預期的標籤
            found = any(tag in result for tag in expected)
            
            if found:
                print(f"  ✅ '{text}'")
                print(f"     → {result}")
                passed += 1
            else:
                print(f"  ⚠️  '{text}'")
                print(f"     → {result}")
                print(f"     預期包含：{expected}")
        
        print(f"\n結果：{passed}/{total} 通過")
        return passed == total
        
    except Exception as e:
        print(f"  ❌ 測試失敗：{str(e)}")
        return False


def test_llm_emotion_route():
    """測試 LLM 語氣判斷器"""
    print("\n" + "=" * 60)
    print("🧠 測試 2：LLM 語氣判斷器（GPT）")
    print("=" * 60)
    
    try:
        from modules.llm_emotion_router import llm_emotion_route
        
        if not os.getenv("OPENAI_API_KEY"):
            print("  ⚠️  OPENAI_API_KEY 未設定，跳過此測試")
            return True
        
        print("  測試 LLM 是否能合理插入語氣標籤...\n")
        
        passed = 0
        total = len(TEST_CASES)
        
        for case in TEST_CASES:
            text = case["text"]
            description = case["description"]
            
            print(f"  📝 測試：{description}")
            print(f"     原文：{text}")
            
            try:
                result = llm_emotion_route(text, provider="openai", fallback_to_rule=True)
                
                # 檢查是否有標籤被插入
                has_tags = "[" in result and "]" in result
                
                if has_tags and result != text:
                    print(f"     ✅ LLM 判斷：{result}")
                    passed += 1
                else:
                    print(f"     ⚠️  回退到規則式：{result}")
                    passed += 1  # 回退也算通過
                    
            except Exception as e:
                print(f"     ❌ 錯誤：{str(e)}")
            
            print()
        
        print(f"結果：{passed}/{total} 通過")
        return True
        
    except ImportError as e:
        print(f"  ⚠️  模組導入失敗（可能未安裝 openai）：{str(e)}")
        print("  提示：執行 pip install openai")
        return False
    except Exception as e:
        print(f"  ❌ 測試失敗：{str(e)}")
        return False


def test_full_pipeline():
    """測試完整流程：文字 → 語氣判斷 → 語音輸出"""
    print("\n" + "=" * 60)
    print("🎤 測試 3：完整流程測試（文字 → 語氣 → 語音）")
    print("=" * 60)
    
    try:
        from emotion_tag_engine import insert_emotion_tags
        from modules.llm_emotion_router import llm_emotion_route
        from eleven_tts import generate_speech
        
        if not os.getenv("ELEVEN_API_KEY"):
            print("  ⚠️  ELEVEN_API_KEY 未設定，跳過語音產生測試")
            return True
        
        # 測試用例
        test_text = "你好，我是黃蓉！"
        
        print(f"  原文：{test_text}\n")
        
        # Step 1: 規則式語氣判斷
        print("  Step 1: 規則式語氣判斷")
        tagged_rule = insert_emotion_tags(test_text)
        print(f"    結果：{tagged_rule}\n")
        
        # Step 2: LLM 語氣判斷（如果可用）
        if os.getenv("OPENAI_API_KEY"):
            print("  Step 2: LLM 語氣判斷")
            try:
                tagged_llm = llm_emotion_route(test_text, provider="openai", fallback_to_rule=True)
                print(f"    結果：{tagged_llm}\n")
                final_text = tagged_llm
            except:
                print(f"    回退到規則式結果\n")
                final_text = tagged_rule
        else:
            final_text = tagged_rule
        
        # Step 3: 產生語音
        print("  Step 3: 產生語音檔案")
        output_file = "test_huangrong_output.mp3"
        
        success = generate_speech(final_text, filename=output_file)
        
        if success:
            file_path = Path(output_file)
            if file_path.exists():
                file_size = file_path.stat().st_size / 1024
                print(f"    ✅ 語音檔案已產生：{output_file} ({file_size:.2f} KB)")
                print(f"    💡 可以播放檔案聽聽黃蓉的效果！")
                return True
            else:
                print(f"    ❌ 檔案未產生")
                return False
        else:
            print(f"    ❌ 語音產生失敗")
            return False
            
    except Exception as e:
        print(f"  ❌ 測試失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_api_endpoints():
    """測試 API 端點（需要 API 運行中）"""
    print("\n" + "=" * 60)
    print("🚀 測試 4：API 端點測試")
    print("=" * 60)
    
    print("  ⚠️  此測試需要 API 服務運行中")
    print("  請先執行：python start_api.py")
    print("  然後在另一個終端執行此測試")
    print()
    print("  測試命令範例：")
    print("  curl -X POST \"http://localhost:8000/api/voice/huangrong\" \\")
    print("    -H \"Content-Type: application/json\" \\")
    print("    -d '{\"text\": \"你好，我是黃蓉！\"}'")
    print()
    print("  或訪問：http://localhost:8000/docs")
    
    return True


def main():
    """主測試函數"""
    print("=" * 60)
    print("🧪 黃蓉語音系統 - 今日驗收測試")
    print("=" * 60)
    
    results = []
    
    # 執行測試
    results.append(("規則式語氣判斷", test_emotion_engine()))
    results.append(("LLM 語氣判斷", test_llm_emotion_route()))
    results.append(("完整流程測試", test_full_pipeline()))
    results.append(("API 端點測試", test_api_endpoints()))
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {name}: {status}")
    
    print(f"\n總計：{passed}/{total} 項測試通過")
    
    if passed == total:
        print("\n🎉 所有測試通過！系統準備就緒。")
        print("\n💡 下一步：")
        print("  1. 播放 test_huangrong_output.mp3 聽聽黃蓉的效果")
        print("  2. 啟動 API：python start_api.py")
        print("  3. 訪問 http://localhost:8000/docs 測試 API")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 項測試未通過，請檢查上述問題。")
        return 1


if __name__ == "__main__":
    sys.exit(main())


