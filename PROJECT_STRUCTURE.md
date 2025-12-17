# 📦 專案檔案說明

## 核心檔案

### `emotion_tag_engine.py`
語氣標籤插入模組，負責根據文字內容自動判斷並插入適當的語氣標籤。

**主要功能：**
- `insert_emotion_tags(text)` - 自動插入語氣標籤
- `insert_emotion_tags_advanced(text, emotion)` - 手動指定語氣標籤
- `AVAILABLE_EMOTION_TAGS` - 可用語氣標籤列表

### `eleven_tts.py`
ElevenLabs v3 API 調用模組，負責與 ElevenLabs API 溝通並產生語音檔案。

**主要功能：**
- `generate_speech()` - 產生語音檔案
- `get_voice_info()` - 取得聲線資訊
- `list_available_voices()` - 列出所有可用聲線

### `main.py`
主執行檔，整合語氣標籤模組與語音輸出功能。

**執行模式：**
- 基本模式：`python main.py` - 執行預設範例
- 互動模式：`python main.py --interactive` - 自行輸入文字

## 設定檔案

### `env.example`
環境變數範例檔案，包含 API Key 和 Voice ID 的設定範本。

**使用方式：**
1. 複製為 `.env` 檔案
2. 填入你的實際 API Key 和 Voice ID

### `.env`（需自行建立）
實際的環境變數檔案，包含敏感的 API 資訊。此檔案已被 `.gitignore` 忽略，不會被提交到 Git。

### `.gitignore`
Git 忽略檔案設定，排除不需要版本控制的檔案（如 `.env`、音訊檔案等）。

## 文件檔案

### `README.md`
專案主要說明文件，包含專案介紹、安裝步驟、使用方式等。

### `QUICKSTART.md`
快速開始指南，提供詳細的步驟說明和常見問題解答。

## 測試檔案

### `test_tools.py`
測試工具，用於測試和調試各個功能模組。

**可用指令：**
- `python test_tools.py emotion` - 測試語氣標籤
- `python test_tools.py voice` - 檢查聲線設定
- `python test_tools.py list` - 列出所有聲線
- `python test_tools.py speech [文字]` - 測試語音產生

## 依賴檔案

### `requirements.txt`
Python 依賴套件清單，包含專案所需的所有套件。

**安裝方式：**
```bash
pip install -r requirements.txt
```

## 專案結構

```
ElevenLabs_v3_alpha/
├── README.md                 # 專案說明文件
├── QUICKSTART.md             # 快速開始指南
├── requirements.txt          # Python 依賴套件
├── env.example                # 環境變數範例
├── .gitignore               # Git 忽略檔案
├── emotion_tag_engine.py    # 語氣標籤插入模組
├── eleven_tts.py            # ElevenLabs API 調用模組
├── main.py                  # 主執行檔
└── test_tools.py            # 測試工具
```

## 開發流程

1. **設定環境**
   - 安裝依賴：`pip install -r requirements.txt`
   - 設定 API：複製 `env.example` 為 `.env` 並填入資訊

2. **測試功能**
   - 執行 `python test_tools.py` 測試各項功能
   - 確認 API 連線和聲線設定正確

3. **使用系統**
   - 執行 `python main.py` 查看範例
   - 或使用 `python main.py --interactive` 進行互動測試

4. **整合應用**
   - 在專案中引入 `emotion_tag_engine` 和 `eleven_tts` 模組
   - 根據需求調整語氣標籤邏輯和語音參數

## 注意事項

- ⚠️ 請妥善保管 `.env` 檔案，不要提交到 Git
- ⚠️ API Key 有使用配額限制，請注意使用量
- 💡 語氣標籤邏輯可以根據實際需求進行擴充和優化
- 💡 語音參數（stability, similarity_boost 等）可以根據效果調整


