"""
🚀 啟動腳本：快速啟動 FastAPI 後端
"""

import uvicorn
import sys
from pathlib import Path

# 確保可以導入模組
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


