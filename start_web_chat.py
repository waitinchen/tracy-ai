"""
啟動 Web 對話界面服務器
"""

import uvicorn
import sys
from pathlib import Path

if __name__ == "__main__":
    print("=" * 60)
    print("🌐 啟動黃蓉語音對話 Web 界面")
    print("=" * 60)
    print("\n服務器將在以下地址啟動：")
    print("  http://localhost:8001")
    print("\n按 Ctrl+C 停止服務器\n")
    
    uvicorn.run(
        "web_chat_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )


