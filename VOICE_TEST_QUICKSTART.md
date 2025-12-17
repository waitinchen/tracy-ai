# 🎤 本地端雙向語音對話測試 - 快速開始

## ✅ 已準備的測試工具

### 1. 快速測試（最簡單）⭐
**檔案：** `quick_voice_test.py`

```bash
py quick_voice_test.py
```

**特點：**
- ✅ 最簡單的對話測試
- ✅ 手動輸入文字
- ✅ 自動處理並播放語音
- ✅ 適合快速驗證功能

---

### 2. 簡化版對話系統
**檔案：** `voice_conversation_simple.py`

```bash
py voice_conversation_simple.py
```

**特點：**
- ✅ 完整的對話循環
- ✅ 詳細的處理過程顯示
- ✅ 支援 LLM 語氣判斷
- ✅ 自動播放語音

---

### 3. 完整版對話系統
**檔案：** `voice_conversation.py`

```bash
# 手動輸入模式
py voice_conversation.py --mode manual

# 語音輸入模式（需要錄音）
py voice_conversation.py --mode voice
```

**特點：**
- ✅ 支援語音輸入（STT）
- ✅ 多種輸入模式
- ✅ 對話歷史記錄
- ✅ 可選 LLM/規則式判斷

---

### 4. 語音轉文字測試
**檔案：** `test_stt.py`

```bash
# 測試語音轉文字
py test_stt.py path/to/audio.mp3
```

**特點：**
- ✅ 測試 Whisper API
- ✅ 支援多種音訊格式
- ✅ 可選擇繼續處理

---

## 🚀 立即開始測試

### 最簡單的方式（推薦）

```bash
py quick_voice_test.py
```

然後輸入測試文字，例如：
```
📝 你說: 你好，我是黃蓉！
```

系統會自動：
1. 加上語氣標籤
2. 產生語音
3. 播放語音

---

## 📋 測試流程

```
1. 語音輸入 (STT)
   ↓
   或手動輸入文字
   ↓
2. 語氣判斷
   - LLM 判斷（如果可用）
   - 或規則式判斷
   ↓
3. 語音產生 (TTS)
   - 呼叫 ElevenLabs API
   ↓
4. 播放語音
   ↓
5. 循環對話
```

---

## 💡 測試建議

1. **首次測試**：使用 `quick_voice_test.py`
2. **完整測試**：使用 `voice_conversation_simple.py`
3. **語音輸入測試**：先錄製音訊，然後使用 `test_stt.py`

---

## 📝 測試範例

### 範例對話

```
📝 你說: 你好，我是黃蓉！
🏷️  [happy] 你好，我是黃蓉！
✅ conv_1234567890.mp3

📝 你說: 你知道嗎？我真的好感動。
🏷️  [crying][softly] 你知道嗎？我真的好感動。
✅ conv_1234567891.mp3

📝 你說: quit
👋 再見！
```

---

## ⚙️ 系統需求

- ✅ Python 3.8+
- ✅ OpenAI API Key（用於 Whisper STT 和 GPT 語氣判斷）
- ✅ ElevenLabs API Key（用於 TTS）
- ✅ 音訊播放器（Windows 內建）

---

## 🎯 測試檢查清單

- [ ] 快速測試通過
- [ ] 文字輸入正常
- [ ] 語氣判斷正常
- [ ] 語音產生正常
- [ ] 語音播放正常
- [ ] 循環對話正常
- [ ] 退出功能正常

---

**準備完成！可以開始測試了！** 🎉


