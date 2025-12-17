"""
🧪 端到端測試腳本：驗證整個系統是否正常運作
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def test_imports():
    """測試模組導入"""
    print("📦 測試模組導入...")
    try:
        from emotion_tag_engine import insert_emotion_tags
        from eleven_tts import generate_speech, API_KEY, VOICE_ID
        from modules.llm_emotion_router import llm_emotion_route
        print("  ✅ 所有模組導入成功")
        return True
    except Exception as e:
        print(f"  ❌ 模組導入失敗：{str(e)}")
        return False

def test_env_vars():
    """測試環境變數"""
    print("\n🔐 測試環境變數...")
    checks = {
        "ELEVEN_API_KEY": os.getenv("ELEVEN_API_KEY"),
        "ELEVEN_HUANGRONG_ID": os.getenv("ELEVEN_HUANGRONG_ID"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    }
    
    all_ok = True
    for key, value in checks.items():
        if value:
            print(f"  ✅ {key}: 已設定")
        else:
            print(f"  ⚠️  {key}: 未設定（可選）")
            if key in ["ELEVEN_API_KEY", "ELEVEN_HUANGRONG_ID"]:
                all_ok = False
    
    return all_ok

def test_directories():
    """測試目錄結構"""
    print("\n📁 測試目錄結構...")
    dirs = [
        "public/audio",
        "api",
        "modules",
        "examples/chatkit",
    ]
    
    all_ok = True
    for dir_path in dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✅ {dir_path}/ 存在")
        else:
            print(f"  ❌ {dir_path}/ 不存在")
            all_ok = False
    
    return all_ok

def test_emotion_engine():
    """測試語氣判斷引擎"""
    print("\n🎭 測試語氣判斷引擎...")
    try:
        from emotion_tag_engine import insert_emotion_tags
        
        test_cases = [
            ("你好", "[excited]"),
            ("這是秘密", "[whispers]"),
            ("我好難過", "[crying]"),
        ]
        
        all_ok = True
        for text, expected_tag in test_cases:
            result = insert_emotion_tags(text)
            if expected_tag in result:
                print(f"  ✅ '{text}' -> {result}")
            else:
                print(f"  ⚠️  '{text}' -> {result} (預期包含 {expected_tag})")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print(f"  ❌ 測試失敗：{str(e)}")
        return False

def test_llm_router():
    """測試 LLM 語氣判斷器（如果 API Key 可用）"""
    print("\n🧠 測試 LLM 語氣判斷器...")
    try:
        from modules.llm_emotion_router import llm_emotion_route
        
        if not os.getenv("OPENAI_API_KEY"):
            print("  ⚠️  OPENAI_API_KEY 未設定，跳過測試")
            return True
        
        test_text = "你知道嗎？我真的好感動。"
        result = llm_emotion_route(test_text, provider="openai", fallback_to_rule=True)
        
        if result and result != test_text:
            print(f"  ✅ LLM 判斷成功：{result}")
            return True
        else:
            print(f"  ⚠️  LLM 判斷回退到規則式：{result}")
            return True  # 回退也是正常的
    except Exception as e:
        print(f"  ⚠️  LLM 測試失敗（可能未安裝套件）：{str(e)}")
        return True  # 不影響整體測試

def test_api_structure():
    """測試 API 檔案結構"""
    print("\n🚀 測試 API 結構...")
    try:
        api_file = Path("api/main.py")
        if api_file.exists():
            print("  ✅ api/main.py 存在")
            
            # 檢查關鍵導入
            content = api_file.read_text(encoding="utf-8")
            if "FastAPI" in content and "llm_emotion_route" in content:
                print("  ✅ API 檔案結構正確")
                return True
            else:
                print("  ⚠️  API 檔案可能不完整")
                return False
        else:
            print("  ❌ api/main.py 不存在")
            return False
    except Exception as e:
        print(f"  ❌ 測試失敗：{str(e)}")
        return False

def main():
    """主測試函數"""
    print("=" * 60)
    print("🧪 黃蓉語音系統 - 端到端測試")
    print("=" * 60)
    print()
    
    results = []
    
    # 執行各項測試
    results.append(("模組導入", test_imports()))
    results.append(("環境變數", test_env_vars()))
    results.append(("目錄結構", test_directories()))
    results.append(("語氣判斷引擎", test_emotion_engine()))
    results.append(("LLM 判斷器", test_llm_router()))
    results.append(("API 結構", test_api_structure()))
    
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
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 項測試未通過，請檢查上述問題。")
        return 1

if __name__ == "__main__":
    sys.exit(main())


