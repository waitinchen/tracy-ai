# 🔧 Web 服務器啟動問題排查指南

## ❌ 問題：無法連接到 http://localhost:8001

### 可能原因與解決方案

#### 1. 服務器未啟動
**解決方案：**
```bash
# 方式 1：使用簡化版啟動腳本
py start_web_simple.py

# 方式 2：直接使用 uvicorn
py -m uvicorn web_chat_api:app --host 127.0.0.1 --port 8001
```

#### 2. 端口被占用
**檢查端口：**
```bash
netstat -ano | findstr :8001
```

**解決方案：**
- 關閉占用端口的程序
- 或使用其他端口（修改啟動腳本中的 port）

#### 3. 防火牆阻擋
**解決方案：**
- 檢查 Windows 防火牆設定
- 暫時關閉防火牆測試
- 允許 Python 通過防火牆

#### 4. 依賴套件未安裝
**安裝依賴：**
```bash
py -m pip install fastapi uvicorn python-dotenv requests
```

---

## ✅ 正確的啟動步驟

### Step 1: 檢查依賴
```bash
py -m pip list | findstr fastapi
py -m pip list | findstr uvicorn
```

### Step 2: 啟動服務器
```bash
py start_web_simple.py
```

### Step 3: 確認啟動成功
應該看到類似訊息：
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001
```

### Step 4: 訪問網址
打開瀏覽器訪問：
```
http://localhost:8001
```
或
```
http://127.0.0.1:8001
```

---

## 🐛 常見錯誤

### 錯誤 1: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'fastapi'
```
**解決：**
```bash
py -m pip install fastapi uvicorn
```

### 錯誤 2: Address already in use
```
Address already in use
```
**解決：**
- 關閉占用端口的程序
- 或修改端口號

### 錯誤 3: ImportError
```
ImportError: cannot import name 'app'
```
**解決：**
- 確認 `web_chat_api.py` 檔案存在
- 確認檔案中有 `app = FastAPI(...)`

---

## 💡 快速測試

### 測試 1: 檢查模組導入
```bash
py -c "from web_chat_api import app; print('OK')"
```

### 測試 2: 檢查端口
```bash
netstat -ano | findstr :8001
```

### 測試 3: 簡單 HTTP 測試
```bash
curl http://localhost:8001/health
```

---

## 🚀 替代啟動方式

### 方式 1: 直接使用 uvicorn
```bash
py -m uvicorn web_chat_api:app --host 127.0.0.1 --port 8001
```

### 方式 2: 使用 Python 內建服務器（僅測試 HTML）
```bash
cd web_static
py -m http.server 8001
```
注意：此方式只能顯示 HTML，無法使用 API 功能

### 方式 3: 檢查並修復
```bash
# 1. 檢查檔案是否存在
dir web_chat_api.py
dir web_static\index.html

# 2. 檢查 Python 版本
py --version

# 3. 重新安裝依賴
py -m pip install --upgrade fastapi uvicorn
```

---

## 📝 啟動檢查清單

- [ ] Python 已安裝
- [ ] 依賴套件已安裝（fastapi, uvicorn）
- [ ] `web_chat_api.py` 檔案存在
- [ ] `web_static/index.html` 檔案存在
- [ ] 端口 8001 未被占用
- [ ] 防火牆允許連接
- [ ] `.env` 檔案已設定

---

## 🎯 如果還是不行

1. **查看完整錯誤訊息**
   - 執行啟動腳本時查看終端輸出
   - 複製錯誤訊息

2. **嘗試其他端口**
   - 修改 `start_web_simple.py` 中的 `port=8001` 改為 `port=8002`
   - 然後訪問 http://localhost:8002

3. **檢查檔案路徑**
   - 確認在正確的目錄執行
   - 確認所有檔案都在專案目錄中


