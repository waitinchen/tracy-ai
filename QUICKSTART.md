# 🚀 快速開始指南

## 步驟 1：安裝依賴套件

```bash
pip install -r requirements.txt
```

## 步驟 2：設定 API 金鑰

1. 前往 [ElevenLabs 官網](https://elevenlabs.io) 註冊並取得 API Key
2. 複製 `env.example` 為 `.env`
3. 編輯 `.env` 檔案，填入你的 API Key 和 Voice ID

```env
ELEVEN_API_KEY=你的_API_Key
ELEVEN_HUANGRONG_ID=你的_Voice_ID
```

### 如何取得 Voice ID？

1. 登入 ElevenLabs 後台
2. 前往 Voices 頁面
3. 選擇或建立「黃蓉」聲線
4. 複製該聲線的 Voice ID（通常是一串字母數字組合）

## 步驟 3：執行範例

### 基本模式（執行預設範例）

```bash
python main.py
```

### 互動模式（自行輸入文字）

```bash
python main.py --interactive
```

## 📝 使用範例

### Python 程式碼中使用

```python
from emotion_tag_engine import insert_emotion_tags
from eleven_tts import generate_speech

# 輸入文字
text = "你知道嗎，我剛剛夢見你在月光下教我輕功"

# 自動插入語氣標籤
tagged_text = insert_emotion_tags(text)
# 結果：[curious] 你知道嗎，我剛剛夢見你在月光下教我輕功

# 產生語音
generate_speech(tagged_text, filename="output.mp3")
```

## 🎭 語氣標籤說明

系統會根據文字內容自動判斷並插入適當的語氣標籤：

| 關鍵字範例 | 插入的標籤 | 效果 |
|-----------|-----------|------|
| 你好、哈囉 | `[excited]` | 興奮的語調 |
| 秘密、悄悄話 | `[whispers]` | 低語/悄悄話 |
| 哭、難過 | `[crying][sighs]` | 哭泣/嘆息 |
| 氣死我、生氣 | `[angry]` | 生氣 |
| 你知道嗎、為什麼 | `[curious]` | 好奇 |
| 其他 | `[speaks quickly][playful]` | 快速/調皮（預設） |

## ⚙️ 進階設定

### 調整語音參數

```python
generate_speech(
    text="你好",
    filename="output.mp3",
    stability=0.5,          # 穩定性（0.0-1.0）
    similarity_boost=0.75,  # 相似度（0.0-1.0）
    style=0.8,              # 風格（0.0-1.0）
    use_speaker_boost=True  # 說話者增強
)
```

### 手動指定語氣標籤

```python
from emotion_tag_engine import insert_emotion_tags_advanced

text = "這是一段文字"
tagged = insert_emotion_tags_advanced(text, emotion="excited")
```

## 🐛 常見問題

### Q: 出現「未設定 ELEVEN_API_KEY」錯誤？
A: 請確認 `.env` 檔案存在且包含正確的 API Key。

### Q: 語音產生失敗？
A: 請檢查：
- API Key 是否有效
- Voice ID 是否正確
- 網路連線是否正常
- ElevenLabs API 配額是否足夠

### Q: 如何加快語速？
A: 在文字開頭加上 `[speaks quickly]` 標籤，或減少句號使用。

## 📚 更多資源

- [ElevenLabs API 文件](https://docs.elevenlabs.io/api-reference/)
- [ElevenLabs 官網](https://elevenlabs.io)


