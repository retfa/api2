# 專案憲章

## 核心原則

- 以維持既有 API 相容性為優先。
- 遷移時只替換 Web framework 邊界，不任意改寫業務邏輯。
- 所有 Markdown 必須使用繁體中文 `zh-TW` 與 `UTF-8`。
- 禁止批量刪除檔案或目錄。

## 架構分層

- `app.py` 負責建立 ASGI app、設定 middleware、註冊 router 與掛載 SocketIO。
- `Controller` 負責 HTTP request/response 邊界。
- `BLL` 負責商業流程與服務協調。
- `DAL` 負責資料存取。
- `Model` 負責 DTO、資料模型與 JWT 相關模型。
- `Kernel` 負責共用處理器。

## 遷移邊界

FastAPI 遷移應避免同時進行資料庫重構、命名重構、目錄重組或未要求的清理。
