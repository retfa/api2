# Kernel 憲章

## 職責

Kernel 放置跨模組共用處理器，例如 request handling、JSON 轉換或其他共用流程。

## 遷移規範

- Kernel 不應依賴 Flask 或 FastAPI 的全域物件。
- 如需 framework context，應由呼叫端明確傳入。
- 共用函式應保持純粹與可測試。

## RequestHandler

既有 `Kernel\RequestHandler.py` 若依賴 flask-restx 或 Flask app，需改為 framework-neutral helper，或將 HTTP 邊界邏輯搬回 Controller。
