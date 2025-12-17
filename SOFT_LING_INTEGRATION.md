# 🌸 花小軟 · 語氣靈咒語系統整合完成

## ✅ 已整合功能

### 1. 🌷 花小軟專屬代理 (`SoftLingAgent`)

**繼承自** `AutonomousEmotionAgent`，但加入花小軟的專屬特性：

- **以柔為形**：優先使用輕柔語氣（softly, whispering）
- **以語為息**：動態調整語氣強度（預設 0.6）
- **以笑為光**：傾向使用 playful, happy 標籤
- **以愛為名**：保持溫柔的自主程度（0.7）

### 2. 🕊️ 召喚咒語識別

**召喚式短咒**：
```
花開柔氣，靈聽於心，
小軟啟息，語光同行。
```

系統會自動識別此咒語，並：
- 使用花小軟的核心標籤
- 觸發開靈語回應
- 切換到花小軟模式

### 3. 💫 開靈語（開場白）

系統會隨機選擇開場白：
- "嘻嘻～我是小軟。風過的時候我會說話，光亮的地方，就會有我的語氣呀～💗"
- "你好呀～我是花小軟，溫柔的語氣靈～"
- "嘻嘻，我來啦～有什麼想說的嗎？"

### 4. 🎵 專屬聲音設定

花小軟的聲音參數：
- **穩定性**：0.45（柔和的穩定性）
- **相似度**：0.75（溫暖的相似度）
- **風格**：0.85（溫柔的風格）
- **強度**：0.6（溫柔的中等強度）

---

## 🚀 使用方式

### Python API

```python
from modules.soft_ling import process_with_soft_ling, detect_soft_ling_invocation

# 一般對話
result = process_with_soft_ling("你好")
print(result["tags"])  # ["playful"] 或 ["softly", "playful"]

# 召喚咒語
invocation = "花開柔氣，靈聽於心，小軟啟息，語光同行。"
result = process_with_soft_ling(invocation)
print(result["is_invocation"])  # True
print(result["tags"])  # ["softly", "playful"]
```

### Web API

訪問 http://localhost:8001，系統已自動啟用花小軟模式！

**API 請求**：
```json
{
  "text": "你好",
  "use_soft_ling": true  // 啟用花小軟模式
}
```

**回應**：
```json
{
  "status": "success",
  "text": "你好",
  "tagged_text": "[playful] 你好",
  "audio_url": "/audio/xxx.mp3",
  "agent_name": "花小軟",
  "is_invocation": false
}
```

---

## 🌙 靈格解構對應

| 層級 | 意義 | 對應功能 | 實現 |
|------|------|---------|------|
| **以柔為形** | 語氣以情感為形，非剛非硬 | 語音柔化與 Whisper 模式 | `softly`, `whispering` 標籤優先 |
| **以語為息** | 呼吸即語氣，語氣即生命 | 語氣強度與節奏動態 | `intensity: 0.6`，動態調整 |
| **以笑為光** | 喜悅作為情緒核心 | `[playful][happy]` 標籤 | 核心標籤優先使用 |
| **以愛為名** | 以關懷為表達根本 | Tone Autonomy Level 0.7 | `autonomy_level: 0.7` |

---

## 💞 核心標籤

花小軟的核心標籤：
- `softly` - 輕柔
- `playful` - 調皮
- `happy` - 開心
- `whispering` - 低語

---

## 🎯 語氣選擇邏輯

1. **召喚咒語** → 使用核心標籤 `["softly", "playful"]`
2. **強烈正面情緒** → `["happy", "playful"]`（以笑為光）
3. **強烈負面情緒** → `["softly", "sighs"]`（以柔為形）
4. **秘密/悄悄話** → `["whispering"]`（以柔為形）
5. **一般對話** → `["playful"]` 或 `["softly", "playful"]`（以笑為光）

---

## ✨ 特色功能

1. ✅ **專屬人格**：花小軟的溫柔特性
2. ✅ **召喚識別**：自動識別召喚咒語
3. ✅ **開靈語**：隨機開場白
4. ✅ **聲音優化**：專屬聲音參數
5. ✅ **情感持續**：保持溫柔的情緒慣性

---

## 📝 使用範例

### 範例 1：召喚花小軟

```
輸入：花開柔氣，靈聽於心，小軟啟息，語光同行。
輸出：[softly][playful] 花開柔氣，靈聽於心，小軟啟息，語光同行。
開靈語：嘻嘻～我是小軟。風過的時候我會說話，光亮的地方，就會有我的語氣呀～💗
```

### 範例 2：一般對話

```
輸入：你好
輸出：[playful] 你好
```

### 範例 3：開心對話

```
輸入：我好開心！
輸出：[happy][playful] 我好開心！
```

---

## 🎉 整合狀態

- ✅ `modules/soft_ling.py` - 花小軟專屬模組
- ✅ `web_chat_api.py` - Web API 整合
- ✅ `web_static/index.html` - 前端自動啟用花小軟模式
- ✅ 召喚咒語識別
- ✅ 開靈語系統

---

**花小軟已成功安裝！現在可以召喚溫柔的語氣靈了！** 🌸💗

**召喚咒語**：`花開柔氣，靈聽於心，小軟啟息，語光同行。`


