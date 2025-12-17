# Proposal: 花小軟 Voice Agent v2.0 模組升級

## Summary

將花小軟 Voice Agent 從測試原型 (v1.0) 升級為可長時間穩定運作的 v2.0。強化語音層快取與重試策略、後端 API 安全與容錯、部署與監控，以及前端播放體驗，並為未來的雙向語音輸入與多角色擴充打好基礎。

## Motivation

- ElevenLabs 呼叫無快取，重複輸出導致延遲與費用攀升。
- 目前缺乏錯誤復原、限流與 API key 維護，無法對外提供穩定服務。
- 音訊檔未清理、部署流程與監控缺席，難以長期運維。
- 前端缺少播放控制、錯誤提示與情緒視覺回饋，互動體驗不足。

## Goals

- 語音 API 平均延遲 < 2s，並支援語氣標籤快取與音訊清理。
- 加入 API key 驗證、速率限制、失敗 fallback 與 log 記錄。
- 建立 Docker 化、CI/CD、自動部署與監控指標上報。
- 前端提供播放控制、歷史紀錄、錯誤提示與情緒視覺。
- 建立 LLM 語氣路由容錯與可配置 voice/model 設定。

## Success Criteria

- [ ] `/api/voice/huangrong` / `/stream` 回應成功率 ≥ 90%，平均延遲 < 2 秒。
- [ ] 對至少 5 種語氣標籤提供快取命中與生成重試。
- [ ] TTL 清理 `public/audio/*.mp3`，快取以 `hash(text+tags)` 命名。
- [ ] 啟用 `SERVICE_API_KEY` 驗證與基本速率限制，並記錄錯誤日誌。
- [ ] Docker + CI/CD Pipeline 完成，提供 Railway / Cloud Run 部署腳本。
- [ ] 前端具有播放/暫停、錯誤提示、情緒標籤與歷史重播。
- [ ] 至少一套自動化測試（unit / integration / e2e）綠燈。
- [ ] 連續 1 小時對話 smoke test 無記憶體異常。

