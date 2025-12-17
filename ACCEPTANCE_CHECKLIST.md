# 🎯 今日驗收任務執行指南

## ✅ 任務 1：執行端到端測試

### 快速執行
```bash
python test_acceptance.py
```

### 或使用快速腳本
```bash
python run_acceptance_tests.py
```

### 驗收重點
- ✅ 從文字 → 語氣判斷 → 語音輸出流程無誤
- ✅ 測試成功後可複製語音檔聽聽黃蓉效果
- ✅ 檢查 `test_huangrong_output.mp3` 是否產生

---

## ✅ 任務 2：啟動並測試 API

### Step 1: 啟動 API
```bash
python start_api.py
```

API 會在 http://localhost:8000 運行

### Step 2: 測試 API（選擇一種方式）

**方式 A：使用測試腳本**
```bash
# 在另一個終端執行
python test_api.py
```

**方式 B：使用 curl**
```bash
# 健康檢查
curl http://localhost:8000/health

# 產生語音
curl -X POST "http://localhost:8000/api/voice/huangrong" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，我是黃蓉！"}'

# 語音流
curl -X POST "http://localhost:8000/api/voice/huangrong/stream" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，我是黃蓉！"}' \
  --output api_output.mp3
```

**方式 C：使用瀏覽器**
訪問 http://localhost:8000/docs 使用 Swagger UI

**方式 D：使用 Postman**
- 方法：POST
- URL：http://localhost:8000/api/voice/huangrong
- Headers：Content-Type: application/json
- Body：
```json
{
  "text": "你好，我是黃蓉！",
  "provider": "openai",
  "emotion_auto": true
}
```

### 驗收重點
- ✅ API 能正常啟動
- ✅ 可以用 curl / Postman / 前端 ChatKit 對接
- ✅ 可加入參數確認功能（如 `?lang=zh` 或 `speaker=huangrong`）

---

## ✅ 任務 3：測試 LLM 語氣判斷

### 快速測試
```python
python -c "from modules.llm_emotion_router import llm_emotion_route; \
print('測試 1:', llm_emotion_route('你知道嗎？我真的好感動。', provider='openai')); \
print('測試 2:', llm_emotion_route('太好了！我們成功了！', provider='openai')); \
print('測試 3:', llm_emotion_route('這是個秘密，不要告訴別人。', provider='openai'))"
```

### 詳細測試
```python
from modules.llm_emotion_router import llm_emotion_route

test_cases = [
    "你知道嗎？我真的好感動。",
    "太好了！我們成功了！",
    "這是個秘密，不要告訴別人。",
    "氣死我了！",
    "你好，我是黃蓉！"
]

for text in test_cases:
    result = llm_emotion_route(text, provider="openai", fallback_to_rule=True)
    print(f"{text}")
    print(f"→ {result}\n")
```

### 標準測試範例

| 輸入 | 預期標籤 | 驗證 |
|------|---------|------|
| "你知道嗎？我真的好感動。" | `[crying][softly]` | ⬜ |
| "太好了！我們成功了！" | `[excited][happy]` | ⬜ |
| "這是個秘密，不要告訴別人。" | `[whispers]` | ⬜ |
| "氣死我了！" | `[angry]` | ⬜ |
| "你好，我是黃蓉！" | `[excited][playful]` | ⬜ |

### 驗收重點
- ✅ GPT 是否能合理插入 [crying], [excited] 等標籤
- ✅ 標籤是否符合語境
- ✅ 記錄標準測試範例，用於自動測試集

---

## 📋 驗收檢查清單

### 功能測試
- [ ] 端到端測試通過
- [ ] 語音檔案成功產生
- [ ] 可以播放語音聽到黃蓉效果
- [ ] API 能正常啟動
- [ ] API 端點正常運作
- [ ] LLM 語氣判斷正常
- [ ] 標籤插入合理

### 測試記錄
- [ ] 記錄測試結果
- [ ] 記錄 LLM 判斷範例
- [ ] 記錄發現的問題（如有）

---

## 🚀 快速執行所有測試

```bash
# 1. 端到端測試
python test_acceptance.py

# 2. 啟動 API（終端 1）
python start_api.py

# 3. API 測試（終端 2）
python test_api.py

# 4. LLM 測試
python -c "from modules.llm_emotion_router import llm_emotion_route; \
[print(f'{t} -> {llm_emotion_route(t, provider=\"openai\")}') \
for t in ['你知道嗎？我真的好感動。', '太好了！我們成功了！', '這是個秘密，不要告訴別人。']]"
```

---

## 💡 驗收完成後

1. **檢查語音檔案**
   - 播放 `test_huangrong_output.mp3`
   - 確認黃蓉聲音效果

2. **記錄測試結果**
   - 填寫測試記錄表
   - 記錄 LLM 判斷範例

3. **準備下一步**
   - 如果測試通過，可以開始整合
   - 如果測試失敗，根據錯誤修復


