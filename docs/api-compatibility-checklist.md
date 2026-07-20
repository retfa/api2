# API 相容性驗收清單

本清單用於確認 Flask 到 FastAPI 遷移後，既有呼叫方不需要修改即可繼續使用。

## HTTP API

- [ ] 所有既有 namespace path 保留。
- [ ] 所有既有 endpoint path 保留。
- [ ] 所有既有 HTTP method 保留。
- [ ] Path parameter 名稱與格式相容。
- [ ] Query parameter 名稱、型別與預設值相容。
- [ ] Request body JSON 欄位相容。
- [ ] Response body 結構相容。
- [ ] 成功與失敗 status code 相容。

## 代表性端點

- [ ] `GET /healthcheck/`
- [ ] `POST /authentication/authenticate`
- [ ] `GET /authentication/whoami`
- [ ] `GET /user/`
- [ ] `GET /permission/`
- [ ] `GET /menu`
- [ ] `GET /menutree/`
- [ ] `GET /machine/`
- [ ] `GET /skyeye/defect`

## JWT 與登入

- [ ] 登入成功時回傳 `jwt` cookie。
- [ ] 登入成功時回傳 `Authorization: Bearer <token>` header。
- [ ] `jwt` cookie 保持 `HttpOnly`。
- [ ] `whoami` 可從 cookie 解出使用者。
- [ ] JWT 過期時回傳相容錯誤。
- [ ] JWT 無效時回傳相容錯誤。

## CORS

- [ ] CORS origins 沿用 `appsettings.json` 的 `CORS` 陣列。
- [ ] Preflight `OPTIONS` 回應允許 `GET, POST, PUT, PATCH, OPTIONS`。
- [ ] Preflight 回應允許 `Content-Type, Authorization`。
- [ ] Credential 行為相容。

## SocketIO

- [ ] 可連線 `/message` namespace。
- [ ] `/message` connect 後收到初始 response。
- [ ] `/message` 背景時間推播正常。
- [ ] 可連線 `/json_message` namespace。
- [ ] 可連線 `/broadcast_message` namespace。
- [ ] Broadcast message 可送達連線 client。

## 文件與打包

- [ ] `/docs` 可開啟。
- [ ] `/openapi.json` 可開啟。
- [ ] `/download-pdf` 行為符合預期。
- [ ] PyInstaller 打包後可啟動。
- [ ] 打包後可讀取 `appsettings.json`。
- [ ] 打包後可讀取 `connections.json`。
- [ ] 打包後可讀取 `security.json`。
