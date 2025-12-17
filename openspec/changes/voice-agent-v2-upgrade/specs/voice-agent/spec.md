# Delta for Voice Agent

## ADDED Requirements

### Requirement: 音訊快取與清理
花小軟 Voice Agent SHALL 快取 ElevenLabs 語音輸出，採用 `hash(原始文字 + 語氣標籤)` 為 key，並在生成成功後儲存至 `public/audio/`。快取項目 MUST 自動於 TTL（預設 1 小時）後清除。

#### Scenario: 快取命中
- GIVEN 使用者輸入的文字與語氣標籤在 1 小時內生成過
- WHEN 後端收到相同輸入
- THEN 系統 SHALL 直接回傳快取音訊 URL，且標記命中

#### Scenario: TTL 清除
- GIVEN 快取音訊建立時間超過 1 小時
- WHEN 清理排程執行
- THEN 系統 MUST 刪除音訊檔案與快取索引

### Requirement: API 安全與容錯
後端 API SHALL 驗證 `SERVICE_API_KEY`，並對單位時間請求數設定速率限制。當 ElevenLabs 或 LLM 呼叫失敗時，系統 MUST 重試並在必要時回退到規則式語氣與文字備援。

#### Scenario: 無效 API key
- GIVEN 使用者未提供或提供錯誤的 `SERVICE_API_KEY`
- WHEN 請求 `/api/voice/huangrong`
- THEN 系統 SHALL 回傳 401 並記錄警示

#### Scenario: 語氣判斷失敗
- GIVEN LLM 語氣判斷超時或失敗
- WHEN 後端處理文字
- THEN 系統 SHALL 使用規則式 `emotion_tag_engine` 產生語氣標籤並繼續流程

### Requirement: 前端播放體驗
前端 SHALL 顯示語氣標籤、音訊播放控制、錯誤提示與歷史紀錄，並於語音生成期間提供載入指示。

#### Scenario: 播放控制
- GIVEN 使用者收到花小軟的語音回應
- WHEN 使用者點擊播放或重播按鈕
- THEN 音訊播放器 MUST 反映狀態（播放/暫停/完成），並允許重新播放

#### Scenario: 錯誤備援
- GIVEN 語音生成失敗
- WHEN 前端收到錯誤回應
- THEN 前端 SHALL 顯示文字備援與再次嘗試按鈕

### Requirement: 部署與監控
系統 SHALL 提供 Docker 化配置、CI/CD pipeline 與部署指南，並收集語音生成延遲、錯誤率與快取命中率。

#### Scenario: 部署腳本
- GIVEN 团队成員欲在 Railway 或 Cloud Run 部署
- WHEN 執行文件內的部署腳本
- THEN 服務 MUST 成功啟動並載入對應 `.env.production`

#### Scenario: 指標上報
- GIVEN 正常對話流程
- WHEN 音訊生成完成或失敗
- THEN 指標服務 MUST 記錄延遲、快取命中、錯誤事件

