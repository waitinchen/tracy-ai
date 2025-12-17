"""
Web 服務器啟動腳本（帶錯誤處理）
"""

import sys
import traceback
from pathlib import Path

print("=" * 60)
print("🌐 啟動黃蓉語音對話 Web 界面")
print("=" * 60)

# 檢查依賴
print("\n📦 檢查依賴套件...")
try:
    import uvicorn
    print("  ✅ uvicorn 已安裝")
except ImportError:
    print("  ❌ uvicorn 未安裝")
    print("  請執行: py -m pip install uvicorn")
    sys.exit(1)

try:
    import fastapi
    print("  ✅ fastapi 已安裝")
except ImportError:
    print("  ❌ fastapi 未安裝")
    print("  請執行: py -m pip install fastapi")
    sys.exit(1)

# 檢查檔案
print("\n📁 檢查檔案...")
if Path("web_chat_api.py").exists():
    print("  ✅ web_chat_api.py 存在")
else:
    print("  ❌ web_chat_api.py 不存在")
    sys.exit(1)

if Path("web_static/index.html").exists():
    print("  ✅ web_static/index.html 存在")
else:
    print("  ⚠️  web_static/index.html 不存在（將創建）")
    Path("web_static").mkdir(exist_ok=True)

# 測試導入
print("\n🔍 測試模組導入...")
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from web_chat_api import app
    print("  ✅ 模組導入成功")
except Exception as e:
    print(f"  ❌ 模組導入失敗: {str(e)}")
    print("\n詳細錯誤：")
    traceback.print_exc()
    sys.exit(1)

# 啟動服務器
print("\n🚀 啟動服務器...")
print("  網址: http://localhost:8001")
print("  按 Ctrl+C 停止服務器\n")
print("=" * 60 + "\n")

try:
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        reload=False,
        log_level="info"
    )
except KeyboardInterrupt:
    print("\n\n👋 服務器已停止")
except Exception as e:
    print(f"\n❌ 啟動失敗: {str(e)}")
    print("\n詳細錯誤：")
    traceback.print_exc()
    sys.exit(1)


