"""
簡化版 Web 服務器啟動腳本
"""

import uvicorn
import sys
from pathlib import Path

# 確保路徑正確
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    print("=" * 60)
    print("🌐 啟動黃蓉語音對話 Web 界面")
    print("=" * 60)
    print("\n服務器將在以下地址啟動：")
    print("  http://localhost:8001")
    print("\n按 Ctrl+C 停止服務器\n")
    
    try:
        uvicorn.run(
            "web_chat_api:app",
            host="127.0.0.1",  # 使用 127.0.0.1 而不是 0.0.0.0
            port=8001,
            reload=False,  # 關閉自動重載，避免問題
            log_level="info"
        )
    except Exception as e:
        print(f"\n❌ 啟動失敗: {str(e)}")
        print("\n請檢查：")
        print("1. 端口 8001 是否被占用")
        print("2. 是否已安裝 uvicorn: pip install uvicorn")
        print("3. 查看上方錯誤訊息")
        sys.exit(1)


