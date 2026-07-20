# DAL 憲章

## 職責

DAL 負責資料庫連線、查詢、交易與資料轉換。

## 遷移規範

- 不應依賴 Flask `current_app`。
- 資料庫連線設定應來自 `connections.json` 或專案設定服務。
- 不應直接處理 HTTP request 或 response。
- 不應在 FastAPI 遷移時改變 SQL 查詢語意。

## 連線設定

`connections.json` 的既有格式必須保留，包含字串型連線與物件型連線設定。
