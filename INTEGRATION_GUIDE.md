# 🧭 黃蓉語音系統升級 v2.0 完整指南

## 📋 專案結構

```
ElevenLabs_v3_alpha/
├── api/
│   └── main.py                    # FastAPI 後端 API
├── modules/
│   └── llm_emotion_router.py      # GPT 語氣判斷器
├── examples/
│   └── chatkit/                   # ChatKit 集成範例
│       ├── HuangrongChat.tsx     # React 組件範例
│       ├── route.ts               # Next.js API Route
│       └── voice-utils.ts         # 工具函數
├── public/
│   └── audio/                     # 音訊檔案儲存目錄
├── emotion_tag_engine.py         # 規則式語氣判斷（備用）
├── eleven_tts.py                 # ElevenLabs API 調用
├── main.py                        # 主執行檔
├── test_tools.py                  # 測試工具
├── requirements.txt               # Python 依賴
├── .env                           # 環境變數（需自行建立）
└── README.md                      # 專案說明
```

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

編輯 `.env` 檔案：

```env
# ElevenLabs API
ELEVEN_API_KEY=sk_09523f3393dfc77d4cfb0b6206fab3f51408668175222c28
ELEVEN_HUANGRONG_ID=0lms72TsW4Q8eDvZttM2

# LLM API（可選，用於自動語氣判斷）
OPENAI_API_KEY=your_openai_key_here
# 或
ANTHROPIC_API_KEY=your_anthropic_key_here

# API 基礎 URL（用於回傳音訊連結）
BASE_URL=http://localhost:8000
```

### 3. 啟動 FastAPI 後端

```bash
# 方式 1：使用 uvicorn
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 方式 2：直接執行
python api/main.py
```

API 文件會自動生成於：http://localhost:8000/docs

## 📡 API 使用說明

### POST /api/voice/huangrong

產生語音並回傳下載 URL。

**請求範例：**

```bash
curl -X POST "http://localhost:8000/api/voice/huangrong" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你今天看起來心情不錯唷～",
    "provider": "openai",
    "emotion_auto": true
  }'
```

**回應範例：**

```json
{
  "status": "success",
  "audio_url": "http://localhost:8000/audio/huangrong_abc123.mp3",
  "text": "你今天看起來心情不錯唷～",
  "tagged_text": "[excited][happy] 你今天看起來心情不錯唷～",
  "message": "語音產生成功"
}
```

### POST /api/voice/huangrong/stream

直接返回音訊流，適合即時播放。

**請求範例：**

```bash
curl -X POST "http://localhost:8000/api/voice/huangrong/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，我是黃蓉！"
  }' \
  --output output.mp3
```

## 🧠 LLM 語氣判斷器

### 使用方式

```python
from modules.llm_emotion_router import llm_emotion_route

# 使用 OpenAI
tagged_text = llm_emotion_route(
    "你知道嗎？我真的好感動。",
    provider="openai",
    fallback_to_rule=True  # LLM 失敗時回退到規則式判斷
)

# 使用 Anthropic Claude
tagged_text = llm_emotion_route(
    "太好了！我們成功了！",
    provider="anthropic",
    fallback_to_rule=True
)
```

### 支援的語氣標籤

- `[excited]` - 興奮
- `[whispers]` - 悄悄話
- `[sarcastic]` - 諷刺
- `[curious]` - 好奇
- `[softly]` - 輕柔
- `[crying]` - 哭泣
- `[starts laughing]` - 開始笑
- `[sings]` - 唱歌
- `[angry]` - 生氣
- `[playful]` - 調皮
- `[speaks quickly]` - 快速說話
- `[sighs]` - 嘆息
- `[happy]` - 開心
- `[sad]` - 難過
- `[surprised]` - 驚訝
- `[whispering]` - 低語
- `[echoes]` - 回音

## 💬 ChatKit 集成

### React/Next.js 範例

參考 `examples/chatkit/HuangrongChat.tsx` 查看完整範例。

**基本使用：**

```tsx
import { playHuangrongVoice } from '@/utils/voice-utils';

// 在組件中
const handlePlayVoice = async () => {
  await playHuangrongVoice({
    text: "你好，我是黃蓉！",
    provider: 'openai',
    emotion_auto: true
  });
};
```

### Next.js API Route

如果使用 Next.js，可以建立 `app/api/voice/huangrong/route.ts` 來轉發請求到 FastAPI 後端。

參考 `examples/chatkit/route.ts`。

## 🔧 進階設定

### 多聲線支援

可以在請求中指定不同的 `voice_id`：

```json
{
  "text": "你好",
  "voice_id": "另一個_voice_id"
}
```

### 關閉自動語氣判斷

```json
{
  "text": "你好",
  "emotion_auto": false
}
```

## 🧪 測試

### 測試 LLM 語氣判斷器

```bash
python modules/llm_emotion_router.py
```

### 測試 API

```bash
# 健康檢查
curl http://localhost:8000/health

# 產生語音
curl -X POST "http://localhost:8000/api/voice/huangrong" \
  -H "Content-Type: application/json" \
  -d '{"text": "測試"}'
```

### 查看 API 文件

訪問 http://localhost:8000/docs 查看互動式 API 文件。

## 📝 注意事項

1. **API Key 安全**：請勿將 `.env` 檔案提交到 Git
2. **LLM 費用**：使用 LLM 語氣判斷會產生 API 費用
3. **回退機制**：如果未設定 LLM API Key，會自動使用規則式判斷
4. **音訊儲存**：產生的音訊檔案會儲存在 `public/audio/` 目錄

## 🚀 部署建議

### 生產環境設定

1. 設定 `BASE_URL` 為實際的域名
2. 限制 CORS 來源（修改 `api/main.py` 中的 `allow_origins`）
3. 使用環境變數管理敏感資訊
4. 考慮使用 Redis 快取常用語音
5. 設定音訊檔案清理機制

## 📚 相關資源

- [ElevenLabs API 文件](https://docs.elevenlabs.io/api-reference/)
- [FastAPI 文件](https://fastapi.tiangolo.com/)
- [OpenAI API 文件](https://platform.openai.com/docs)
- [Anthropic API 文件](https://docs.anthropic.com/)


