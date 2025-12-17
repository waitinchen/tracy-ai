"""
直接啟動 Web 服務器（最簡單版本）
"""

if __name__ == "__main__":
    import uvicorn
    from web_chat_api import app
    
    print("=" * 60)
    print("啟動 Web 服務器...")
    print("訪問: http://localhost:8001")
    print("按 Ctrl+C 停止")
    print("=" * 60)
    
    uvicorn.run(app, host="127.0.0.1", port=8001)


