# Auth 與 JWT 憲章

## 職責

Auth 與 JWT 模組負責登入驗證、JWT 產生、JWT 解碼、cookie 與 header 相容行為。

## 相容性規範

- 登入 API 必須保留 `jwt` cookie。
- 登入 API 必須保留 `Authorization: Bearer <token>` response header。
- Cookie 必須保持 `HttpOnly`。
- JWT payload 欄位必須保留：`FTASn`、`FTAId`、`YFYId`、`Name`、`exp`、`iat`、`nbf`、`jti`、`iss`、`aud`。
- JWT expiration 必須沿用 `appsettings.json`。
- JWT key 與 issuer 必須沿用 `security.json`。

## FastAPI 遷移規範

- 不得使用 Flask `request`。
- 解碼 JWT 時應從 FastAPI `Request` 讀取 cookie 或 header。
- 回應 cookie/header 時應使用 FastAPI `Response` 或 `JSONResponse`。
