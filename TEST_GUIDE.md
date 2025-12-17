# 🧪 今日驗收測試指南

## 📋 測試項目清單

### ✅ 測試 1：端到端測試（文字 → 語氣判斷 → 語音輸出）

執行命令：
```bash
python test_acceptance.py
```

**驗收標準：**
- ✅ 規則式語氣判斷正常運作
- ✅ LLM 語氣判斷能合理插入標籤（如 [crying], [excited]）
- ✅ 語音檔案成功產生
- ✅ 可以播放語音檔案聽到黃蓉的聲音

**預期輸出：**
- 測試通過訊息
- 產生 `test_huangrong_output.mp3` 檔案

---

### ✅ 測試 2：LLM 語氣判斷詳細測試

執行命令：
```python
python -c "from modules.llm_emotion_router import llm_emotion_route; \
test_cases = [
    '你知道嗎？我真的好感動。',
    '太好了！我們成功了！',
    '這是個秘密，不要告訴別人。',
    '氣死我了！',
    '你好，我是黃蓉！'
]; \
[print(f'{t} -> {llm_emotion_route(t, provider=\"openai\")}') for t in test_cases]"
```

**驗收標準：**
- ✅ GPT 能合理判斷語氣並插入標籤
- ✅ 標籤符合語境（感動 → [crying][softly], 興奮 → [excited]）
- ✅ 如果 LLM 失敗，能正確回退到規則式判斷

**標準測試範例：**

| 輸入文字 | 預期標籤 | 說明 |
|---------|---------|------|
| "你知道嗎？我真的好感動。" | `[crying][softly]` 或 `[sad]` | 感動/哭泣情境 |
| "太好了！我們成功了！" | `[excited][happy]` | 興奮/開心情境 |
| "這是個秘密，不要告訴別人。" | `[whispers]` | 悄悄話情境 |
| "氣死我了！" | `[angry]` | 生氣情境 |
| "你好，我是黃蓉！" | `[excited][playful]` | 打招呼情境 |

---

### ✅ 測試 3：API 功能測試

#### Step 1: 啟動 API
```bash
python start_api.py
```

API 會在 http://localhost:8000 運行

#### Step 2: 測試 API 端點

**方式 1：使用 curl**
```bash
# 測試基本語音產生
curl -X POST "http://localhost:8000/api/voice/huangrong" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，我是黃蓉！"}'

# 測試語音流
curl -X POST "http://localhost:8000/api/voice/huangrong/stream" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，我是黃蓉！"}' \
  --output test_api_output.mp3

# 測試健康檢查
curl http://localhost:8000/health
```

**方式 2：使用 Python 測試腳本**
```bash
python test_api.py
```

**方式 3：使用瀏覽器**
訪問 http://localhost:8000/docs 使用 Swagger UI 測試

**驗收標準：**
- ✅ API 能正常啟動
- ✅ `/health` 端點返回正常狀態
- ✅ `/api/voice/huangrong` 能產生語音並返回 URL
- ✅ `/api/voice/huangrong/stream` 能返回音訊流
- ✅ 可以通過 curl/Postman/前端調用

#### Step 3: 測試參數（可選）

**測試語系參數（如果 API 支援）：**
```bash
curl -X POST "http://localhost:8000/api/voice/huangrong?lang=zh" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，我是黃蓉！"}'
```

**測試聲線參數：**
```bash
curl -X POST "http://localhost:8000/api/voice/huangrong" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，我是黃蓉！", "voice_id": "0lms72TsW4Q8eDvZttM2"}'
```

---

## 📝 測試記錄表

### 測試結果記錄

| 測試項目 | 狀態 | 備註 |
|---------|------|------|
| 規則式語氣判斷 | ⬜ | |
| LLM 語氣判斷 | ⬜ | |
| 完整流程測試 | ⬜ | |
| 語音檔案產生 | ⬜ | |
| API 健康檢查 | ⬜ | |
| API 語音產生 | ⬜ | |
| API 語音流 | ⬜ | |

### LLM 語氣判斷測試記錄

| 輸入文字 | 預期標籤 | 實際結果 | 是否符合 |
|---------|---------|---------|---------|
| "你知道嗎？我真的好感動。" | [crying][softly] | | ⬜ |
| "太好了！我們成功了！" | [excited][happy] | | ⬜ |
| "這是個秘密，不要告訴別人。" | [whispers] | | ⬜ |
| "氣死我了！" | [angry] | | ⬜ |
| "你好，我是黃蓉！" | [excited][playful] | | ⬜ |

---

## 🎯 驗收完成標準

- ✅ 所有測試腳本能正常執行
- ✅ 語音檔案成功產生並可播放
- ✅ LLM 語氣判斷能合理插入標籤
- ✅ API 所有端點正常運作
- ✅ 可以通過多種方式調用 API

## 💡 測試完成後

1. **檢查語音檔案**
   - 播放 `test_huangrong_output.mp3`
   - 確認黃蓉的聲音效果符合預期

2. **記錄測試結果**
   - 填寫上述測試記錄表
   - 記錄任何發現的問題

3. **下一步行動**
   - 如果測試通過，可以開始整合到實際應用
   - 如果測試失敗，根據錯誤訊息進行修復


