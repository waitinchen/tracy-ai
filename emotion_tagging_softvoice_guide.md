# 🎯 技術指引：小軟語音表演 × ElevenLabs v3 情緒標籤調用指南

## 📁 文件名稱：`emotion_tagging_softvoice_guide.md`

---

## 一、🧠 背景說明：語氣靈不是朗讀，是表演

> 小軟不是單純 TTS（文字轉語音），而是 Voice Agent with Emotion Intelligence。
>
> 本技術指引以《小軟開場介紹》段落為例，示範如何在 LLM 輸出文字中自動插入 **ElevenLabs v3 的 Audio Tags**，讓語音有情緒、有戲、有溫度。

---

## 二、🎭 小軟語氣類型 × 對應情緒標籤

| 小軟語氣描述 | ElevenLabs 標籤                     | 可疊加參數                 | 範例位置       |
| ------ | --------------------------------- | --------------------- | ---------- |
| 快速講話   | `[speed:fast]`                    | 可與 excited 疊加         | 嗨～大家好呀…    |
| 撒嬌俏皮   | `[style:playful]`                 | 可疊加 soft / high_pitch | 你也可以叫我～    |
| 冷笑調侃   | `[style:sarcastic]`               | 可混合低語速                | 嗯哼…是不是…    |
| 好奇探問   | `[style:curious]`                 | 可加中速、提高 pitch         | 不急，我來說…    |
| 低語解釋   | `[style:whispering] [speed:fast]` | 可加 soft               | GPT 是語言模型… |
| 嚴肅斷言   | `[style:serious]`                 | 可搭配 strong emphasis   | 它，沒有語氣。    |
| 英式驚嘆   | `[accent:british] [speed:fast]`   | 可加 style:dramatic     | Imagine…   |
| 自信堅定   | `[style:confident]`               |                       | 而我，來自語氣靈…  |
| 柔和安慰   | `[style:soft] [style:whispering]` |                       | 沒事的，我懂你。   |
| 哭泣情緒   | `[style:crying] [breath:heavy]`   | 可加 slow               | 哭出來…       |
| 笑聲插入   | `[laugh]`                         | 可置於任意點                | 哈哈～我不是…    |
| 惡作劇鬧   | `[style:mischievous]`             | 可加 high_pitch         | 喂喂喂～我不是…   |
| 唱歌     | `[singing]`                       | 適合斷句處                 | 用愛說話的能力～   |
| 響亮結語   | `[echo]`                          | 可加 confident          | 謝謝大家～      |

---

## 三、🛠️ 應用方式：自動語氣標籤系統設計建議

### 📍 模組檔案：`emotion_tag_engine.py`

* 輸入：LLM 輸出原始文字（有語氣說明提示詞）
* 處理邏輯：
  1. 掃描標準語氣提示（如：`[sarcastic]`）
  2. 根據表情詞、動詞語氣、語者角色自動標記
  3. 插入 `ElevenLabs Audio Tags` 語法
* 輸出：已標記情緒標籤的文字供 TTS API 使用

### 📍 語氣特徵對照表（簡化版）

| 語氣提示 | 自動對應標籤                            |
| ---- | --------------------------------- |
| 撒嬌   | `[style:playful]`                 |
| 嚴肅   | `[style:serious]`                 |
| 哭    | `[style:crying]`                  |
| 快樂   | `[style:excited]`                 |
| 偷笑   | `[style:mischievous]`             |
| 安慰   | `[style:soft] [style:whispering]` |

---

## 四、📦 快速整合方式（給 C謀）

### 可調用的參數語法範例：

```python
text = "[sarcastic][speed:slow] 哼哼，你是不是以為我只是 GPT 的分身？"

audio = generate_elevenlabs_audio(text, voice_id="xiaoruan_v3", output_voice_tag="huangrong-v3-output")
```

---

## 五、📍 建議工作流程

1. 🧠 ChatGPT/Claude → 先產生文字 + 標註語氣說明（例：`[小軟：撒嬌地說]`）
2. 🔧 `emotion_tag_engine.py` → 將語氣說明自動轉成 ElevenLabs v3 Audio Tags
3. 🗣️ `eleven_tts.py` → 呼叫 v3 語音合成，套用黃蓉或小軟 Voice ID
4. 🎧 `stream_audio.py` → 回傳給使用者串流播放

