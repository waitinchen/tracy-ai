# 🎤 本地端雙向語音對話測試指南

## 📋 測試準備

### 1. 安裝依賴

```bash
py -m pip install openai python-dotenv requests
```

### 2. 確認環境變數

確保 `.env` 檔案包含：
```env
ELEVEN_API_KEY=your_key
ELEVEN_HUANGRONG_ID=your_voice_id
OPENAI_API_KEY=your_openai_key  # 用於 Whisper STT 和 GPT 語氣判斷
```

---

## 🎯 測試方式

### 方式 1：簡化版對話測試（推薦開始）

**最簡單的方式，使用手動輸入模擬語音對話**

```bash
py voice_conversation_simple.py
```

**功能：**
- ✅ 手動輸入文字
- ✅ 自動加上語氣標籤
- ✅ 產生語音並播放
- ✅ 循環對話

**使用流程：**
1. 執行腳本
2. 輸入文字（例如："你好，我是黃蓉！"）
3. 系統自動處理並播放語音
4. 繼續輸入下一句，或輸入 'quit' 結束

---

### 方式 2：完整版對話系統

**支援語音輸入（需要錄音）**

```bash
# 手動輸入模式
py voice_conversation.py --mode manual

# 語音輸入模式（需要先錄製音訊）
py voice_conversation.py --mode voice

# 不使用 LLM，只用規則式判斷
py voice_conversation.py --no-llm
```

---

### 方式 3：語音轉文字測試

**測試語音輸入功能**

```bash
# 方式 A: 提供音訊檔案
py test_stt.py path/to/audio.mp3

# 方式 B: 互動式（會提示輸入檔案路徑）
py test_stt.py
```

**支援的音訊格式：**
- .mp3
- .wav
- .m4a
- .webm

---

## 🔄 完整對話流程

```
1. 語音輸入 (STT)
   ↓
2. 文字處理（語氣判斷）
   ↓
3. 語音輸出 (TTS)
   ↓
4. 播放語音
   ↓
5. 循環回到步驟 1
```

---

## 📝 測試範例

### 範例 1：基本對話

```bash
py voice_conversation_simple.py
```

**對話範例：**
```
📝 你說: 你好，我是黃蓉！
🔄 處理中...
🏷️  標籤後: [happy] 你好，我是黃蓉！
🎵 產生語音中...
✅ 語音已產生: conversation_1234567890.mp3
🔊 播放語音...

📝 你說: 你知道嗎？我真的好感動。
🔄 處理中...
🏷️  標籤後: [crying][softly] 你知道嗎？我真的好感動。
🎵 產生語音中...
✅ 語音已產生: conversation_1234567891.mp3
🔊 播放語音...

📝 你說: quit
👋 對話結束！
```

---

### 範例 2：語音輸入測試

**Step 1: 錄製語音**
- 使用 Windows 語音錄音機錄製一段話
- 儲存為 `test_voice.wav`

**Step 2: 轉換為文字**
```bash
py test_stt.py test_voice.wav
```

**Step 3: 繼續處理**
- 系統會詢問是否繼續處理
- 輸入 'y' 會自動加上語氣標籤並產生語音

---

## 🎙️ 錄音工具推薦

### Windows 內建工具
1. **語音錄音機**（Windows 10/11）
   - 開始選單搜尋「語音錄音機」
   - 點擊錄音按鈕
   - 儲存為 .m4a 格式

2. **命令提示字元錄音**
   ```bash
   # 使用 PowerShell
   Start-Process "ms-settings:sound"
   ```

### 第三方工具
- **Audacity**（免費，功能強大）
- **OBS Studio**（免費，可錄音）
- **QuickTime Player**（Mac）

---

## ⚙️ 進階設定

### 使用本地 Whisper（不需要 API）

```bash
# 安裝本地 Whisper
pip install openai-whisper

# 使用本地模型
# voice_conversation.py 會自動偵測並使用本地 Whisper
```

### 麥克風即時錄音（需要額外套件）

```bash
# 安裝音訊處理套件
pip install pyaudio sounddevice

# 修改 voice_conversation.py 添加即時錄音功能
```

---

## 🐛 常見問題

### Q: 語音播放失敗？
A: 
- Windows: 系統會自動使用預設播放器
- 如果失敗，請手動開啟產生的 .mp3 檔案

### Q: Whisper API 錯誤？
A: 
- 確認 OPENAI_API_KEY 已設定
- 確認音訊檔案格式支援
- 確認網路連線正常

### Q: 語音產生失敗？
A: 
- 確認 ELEVEN_API_KEY 已設定
- 確認 ELEVEN_HUANGRONG_ID 已設定
- 檢查 API 配額

---

## 📊 測試檢查清單

- [ ] 簡化版對話測試通過
- [ ] 語音轉文字功能正常
- [ ] 語氣判斷正常運作
- [ ] 語音產生正常
- [ ] 語音播放正常
- [ ] 循環對話正常
- [ ] 退出功能正常

---

## 🚀 快速開始

**最簡單的測試方式：**

```bash
# 1. 執行簡化版對話測試
py voice_conversation_simple.py

# 2. 輸入測試文字
📝 你說: 你好，我是黃蓉！

# 3. 等待語音產生並播放

# 4. 繼續對話或輸入 'quit' 結束
```

---

## 💡 提示

1. **首次測試建議使用簡化版**（`voice_conversation_simple.py`）
2. **確認所有 API Key 已設定**
3. **測試時建議使用短句**（避免語音檔案過大）
4. **可以隨時輸入 'quit' 結束對話**


