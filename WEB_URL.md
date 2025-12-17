# 🌐 本地 Web 對話界面 - 快速訪問

## 🚀 訪問網址

### 本地對話界面
```
http://localhost:8001
```

或

```
http://127.0.0.1:8001
```

---

## 📋 啟動方式

### 方式 1：使用啟動腳本（推薦）
```bash
py start_web_chat.py
```

### 方式 2：直接啟動
```bash
py -m uvicorn web_chat_api:app --host 0.0.0.0 --port 8001 --reload
```

---

## ✅ 確認服務器運行

訪問健康檢查端點：
```
http://localhost:8001/health
```

應該看到：
```json
{
  "status": "healthy",
  "api_key_set": true,
  "voice_id_set": true
}
```

---

## 🎯 使用步驟

1. **啟動服務器**
   ```bash
   py start_web_chat.py
   ```

2. **打開瀏覽器**
   - 訪問 http://localhost:8001

3. **開始對話**
   - 輸入文字
   - 點擊發送或按 Enter
   - 聽黃蓉說話！

---

## 💡 功能特色

- ✅ 美觀的 Web 界面
- ✅ 即時對話
- ✅ 自動語音播放
- ✅ 顯示語氣標籤
- ✅ 響應式設計

---

**準備完成！訪問 http://localhost:8001 開始對話！** 🎉


