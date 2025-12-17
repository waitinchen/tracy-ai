"""
🚀 快速驗收執行腳本

一鍵執行所有驗收測試
"""

import subprocess
import sys
import time

def run_test(test_name, command):
    """執行測試並顯示結果"""
    print("\n" + "=" * 60)
    print(f"🧪 {test_name}")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 執行錯誤：{str(e)}")
        return False

def main():
    """主函數"""
    print("=" * 60)
    print("🎯 黃蓉語音系統 - 今日驗收測試")
    print("=" * 60)
    print("\n此腳本將執行以下測試：")
    print("1. 端到端測試（文字 → 語氣 → 語音）")
    print("2. LLM 語氣判斷測試")
    print("3. API 測試（需要 API 運行中）")
    print("\n開始執行...")
    
    results = []
    
    # 測試 1: 端到端測試
    results.append((
        "端到端測試",
        run_test("端到端測試", "python test_acceptance.py")
    ))
    
    # 測試 2: LLM 語氣判斷（單獨測試）
    print("\n" + "=" * 60)
    print("🧠 LLM 語氣判斷詳細測試")
    print("=" * 60)
    
    test_cases = [
        "你知道嗎？我真的好感動。",
        "太好了！我們成功了！",
        "這是個秘密，不要告訴別人。",
        "氣死我了！",
        "你好，我是黃蓉！"
    ]
    
    try:
        from modules.llm_emotion_router import llm_emotion_route
        
        print("\n測試 LLM 語氣判斷...\n")
        for text in test_cases:
            result = llm_emotion_route(text, provider="openai", fallback_to_rule=True)
            print(f"  {text}")
            print(f"  → {result}\n")
        
        results.append(("LLM 語氣判斷", True))
    except Exception as e:
        print(f"  ⚠️  LLM 測試跳過：{str(e)}")
        results.append(("LLM 語氣判斷", False))
    
    # 測試 3: API 測試（提示）
    print("\n" + "=" * 60)
    print("🚀 API 測試")
    print("=" * 60)
    print("\n⚠️  API 測試需要服務運行中")
    print("請執行以下步驟：")
    print("1. 在另一個終端執行：python start_api.py")
    print("2. 等待 API 啟動完成")
    print("3. 執行：python test_api.py")
    print("\n或訪問：http://localhost:8000/docs")
    
    results.append(("API 測試", None))  # 手動測試
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    
    for name, result in results:
        if result is None:
            status = "⏭️  需手動測試"
        elif result:
            status = "✅ 通過"
        else:
            status = "❌ 失敗"
        print(f"  {name}: {status}")
    
    print("\n💡 下一步：")
    print("  1. 播放 test_huangrong_output.mp3 聽聽黃蓉效果")
    print("  2. 啟動 API：python start_api.py")
    print("  3. 執行 API 測試：python test_api.py")

if __name__ == "__main__":
    main()


