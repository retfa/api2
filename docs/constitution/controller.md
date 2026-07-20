# Controller 憲章

## 職責

Controller 負責 HTTP API 邊界，包含路由、request parsing、response 建立、status code、cookie 與 header。

## 遷移規範

- flask-restx `Namespace` 必須改為 FastAPI `APIRouter`。
- flask-restx `Resource` method 必須改為 router function。
- 不得改變公開 URL。
- 不得改變既有 HTTP method。
- 不得任意改變 response body 結構。
- Flask `request` 必須改為 FastAPI `Request` 或明確參數。

## 錯誤處理

- 原本回傳 dict 與 status code tuple 的地方，FastAPI 應使用相容的 response。
- 例外訊息格式應盡量保留，避免前端解析失敗。
