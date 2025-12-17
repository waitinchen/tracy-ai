# 🎵 語氣標籤 → 聲音參數映射整合指南

## ✅ 整合完成

已成功整合語氣標籤到 ElevenLabs 聲音參數的映射層！

---

## 📁 新增檔案

### 1. `modules/speech_tag_mapper.py`
- **功能**：將語氣標籤轉換為 ElevenLabs voice_settings 參數
- **核心函數**：
  - `map_tags_to_voice_settings()` - 標籤 → 聲音參數
  - `extract_tags_from_text()` - 從文字提取標籤
  - `process_text_with_voice_settings()` - 完整處理流程

### 2. `modules/voice_engine.py`
- **功能**：整合範例，展示完整流程
- **核心函數**：
  - `speak_with_autonomous_emotion()` - 完整語音生成流程
  - `analyze_emotion()` - 情緒分析（與用戶範例格式一致）

---

## 🔄 整合流程

```
用戶輸入文字
    ↓
autonomous_emotion.py → 自主判斷語氣標籤
    ↓
speech_tag_mapper.py → 將標籤映射為聲音參數
    ↓
eleven_tts.py → 調用 ElevenLabs API（使用映射的參數）
    ↓
生成語音檔案
```

---

## 🎯 核心功能

### 1. 標籤映射邏輯

不同語氣標籤會映射到不同的聲音參數：

| 標籤 | stability | similarity_boost | style | use_speaker_boost |
|------|-----------|------------------|-------|------------------|
| crying | 0.3 | 0.7 | 0.95 | True |
| excited | 0.5 | 0.85 | 0.95 | True |
| whispers | 0.25 | 0.6 | 0.7 | False |
| playful | 0.5 | 0.85 | 0.9 | True |
| angry | 0.35 | 0.75 | 0.95 | True |

### 2. 多標籤處理

當有多個標籤時，系統會：
- 計算加權平均
- 強烈情緒標籤權重更高（1.5x）
- 自動調整參數範圍

### 3. 自動整合

- `eleven_tts.py` 已更新，支援自動標籤映射
- `web_chat_api.py` 已更新，自動使用映射的聲音參數
- 保持向後兼容，不破壞現有功能

---

## 🚀 使用方式

### 方式 1：直接使用映射器

```python
from modules.speech_tag_mapper import map_tags_to_voice_settings

tags = ["crying", "curious"]
voice_settings = map_tags_to_voice_settings(tags)
# => {"stability": 0.375, "similarity_boost": 0.75, ...}
```

### 方式 2：使用整合函數

```python
from modules.voice_engine import speak_with_autonomous_emotion

speak_with_autonomous_emotion(
    text="你知道嗎？我真的好感動。",
    autonomy_level=0.7,
    output_filename="output.mp3"
)
```

### 方式 3：Web API（已自動整合）

訪問 http://localhost:8001，系統會自動：
1. 自主判斷語氣
2. 映射聲音參數
3. 生成語音

---

## 📊 映射規則說明

### 穩定性 (stability)
- **低**（0.25-0.35）：情緒強烈、輕柔聲音
- **中**（0.4-0.5）：一般情緒、調皮
- **高**（0.6+）：快速說話、穩定表達

### 相似度 (similarity_boost)
- **低**（0.6-0.7）：輕柔、特殊效果
- **中**（0.75-0.8）：一般情緒
- **高**（0.85+）：強烈情緒、活潑

### 風格 (style)
- **低**（0.7-0.8）：輕柔、特殊效果
- **中**（0.85-0.9）：一般情緒
- **高**（0.95）：強烈情緒、驚訝

### 說話者增強 (use_speaker_boost)
- **True**：強烈情緒、活潑表達
- **False**：輕柔、特殊效果

---

## 🧪 測試

執行測試腳本：

```bash
py modules/speech_tag_mapper.py
```

測試結果會顯示：
- 不同標籤的聲音參數映射
- 多標籤的加權平均計算
- 文字標籤提取功能

---

## ✨ 特色功能

1. **智能映射**：根據語氣標籤自動調整聲音參數
2. **多標籤支援**：處理多個標籤的組合
3. **加權平均**：強烈情緒標籤權重更高
4. **自動整合**：無需修改現有代碼即可使用
5. **向後兼容**：不破壞現有功能

---

## 🔧 進階配置

### 自定義映射

修改 `modules/speech_tag_mapper.py` 中的 `tag_mappings` 字典：

```python
tag_mappings = {
    "your_tag": {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.9,
        "use_speaker_boost": True
    }
}
```

### 調整基礎參數

```python
voice_settings = map_tags_to_voice_settings(
    tags,
    base_stability=0.5,      # 調整基礎穩定性
    base_similarity_boost=0.8, # 調整基礎相似度
    base_style=0.9            # 調整基礎風格
)
```

---

## 📝 注意事項

1. **標籤格式**：ElevenLabs v3 使用 `[tag]` 格式的標籤
2. **參數範圍**：所有參數都在 0.0-1.0 範圍內
3. **文字保留**：標籤會保留在文字中，ElevenLabs 會處理
4. **參數覆蓋**：映射的參數會覆蓋預設值

---

**整合完成！系統現在可以自動將語氣標籤轉換為對應的聲音參數了！** 🎤✨


