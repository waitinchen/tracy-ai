# 🚀 Web 服務器啟動指南

## ✅ 推薦啟動方式

### 方式 1：使用調試版啟動腳本（推薦）
```bash
py start_web_debug.py
```

這個腳本會：
- ✅ 檢查依賴套件
- ✅ 檢查必要檔案
- ✅ 測試模組導入
- ✅ 顯示詳細錯誤訊息

### 方式 2：使用簡化版啟動腳本
```bash
py start_web_simple.py
```

### 方式 3：直接使用 uvicorn
```bash
py -m uvicorn web_chat_api:app --host 127.0.0.1 --port 8001
```

---

## 🔍 檢查步驟

### Step 1: 確認依賴已安裝
```bash
py -m pip install fastapi uvicorn python-dotenv requests
```

### Step 2: 確認檔案存在
```bash
dir web_chat_api.py
dir web_static\index.html
```

### Step 3: 測試導入
```bash
py -c "from web_chat_api import app; print('OK')"
```

### Step 4: 啟動服務器
```bash
py start_web_debug.py
```

---

## 📋 啟動成功標誌

啟動成功時，應該看到：
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
```

---

## 🌐 訪問網址

啟動成功後，訪問：
```
http://localhost:8001
```
或
```
http://127.0.0.1:8001
```

---

## 🐛 如果還是無法連接

1. **檢查服務器是否真的啟動**
   - 查看終端是否有錯誤訊息
   - 確認看到 "Uvicorn running" 訊息

2. **檢查端口是否被占用**
   ```bash
   netstat -ano | findstr :8001
   ```

3. **嘗試其他端口**
   - 修改啟動腳本中的 `port=8001` 改為 `port=8002`
   - 然後訪問 http://localhost:8002

4. **檢查防火牆**
   - Windows 防火牆可能阻擋連接
   - 暫時關閉測試

---

## 💡 快速測試命令

```bash
# 測試健康檢查端點
curl http://localhost:8001/health

# 或使用 PowerShell
Invoke-WebRequest -Uri http://localhost:8001/health
```

---

**請執行 `py start_web_debug.py` 並查看輸出訊息！** 🔍


