# Tasks: 花小軟 Voice Agent v2.0 模組升級

## 1. 語音層快取與清理
- [ ] 1.1 建立文字+語氣標籤為 key 的音訊快取模組
- [ ] 1.2 新增 TTL 清理排程，移除超過 1 小時的 `public/audio/*.mp3`
- [ ] 1.3 ElevenLabs 呼叫加入 retry/backoff 與錯誤 fallback (文字提示或預設語音)
- [ ] 1.4 紀錄生成延遲與快取命中率 (log/metrics)

## 2. 後端 API 健壯性
- [ ] 2.1 為 `/api/voice/huangrong` 与 `/stream` 添加 `SERVICE_API_KEY` 驗證與速率限制
- [ ] 2.2 LLM 標籤失敗時 fallback 至規則式 `emotion_tag_engine`
- [ ] 2.3 建立錯誤日誌與告警（Sentry 或 loguru + webhook）
- [ ] 2.4 撰寫單元 / 整合測試覆蓋快取、重試與 fallback

## 3. 部署與監控
- [ ] 3.1 撰寫 Dockerfile、docker-entrypoint 與 `.dockerignore`
- [ ] 3.2 建立 `.env.dev` / `.env.production` 並在 README 說明
- [ ] 3.3 設定 Railway / Cloud Run 部署腳本與 CI/CD（GitHub Actions）
- [ ] 3.4 收集核心指標：生成次數、錯誤率、延遲；提供簡易監控/告警

## 4. 前端互動體驗
- [ ] 4.1 新增播放/暫停/重播控制與載入狀態
- [ ] 4.2 提供語音失敗的文字備援與錯誤提示
- [ ] 4.3 顯示語氣標籤圖示 / 顏色變化，並保留歷史清單可重播
- [ ] 4.4 串接情緒視覺狀態（粒子/背景隨標籤變化）

## 5. 文件與驗收
- [ ] 5.1 更新 README / docs，描述部署、環境、操作與維運
- [ ] 5.2 撰寫 smoke test / 壓力測試腳本並驗證 1 小時穩定度
- [ ] 5.3 完成 OpenSpec 變更驗收，將 delta 合併到正式 spec

