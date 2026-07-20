# Flask 到 FastAPI 遷移需求規格

## 目標

將目前 Flask 與 flask-restx 架構完整遷移為 FastAPI 原生架構，並保持既有 HTTP API 與 SocketIO 使用者的行為相容。

## 範圍

- 改寫 `app.py` 為 FastAPI ASGI app。
- 將 `Controller/*.py` 的 flask-restx `Namespace` 與 `Resource` 改為 FastAPI `APIRouter`。
- 將 Flask `request`、`Response`、`make_response`、`current_app` 等依賴替換為 FastAPI 或專案自有介面。
- 將 SocketIO 改為 ASGI 掛載。
- 更新 `requirements.txt` 與 PyInstaller spec。
- 更新 API 文件與驗收清單。

## 非目標

- 不重新設計資料庫 schema。
- 不改寫核心業務邏輯。
- 不重新命名既有公開 URL。
- 不引入非必要的非同步資料庫存取。
- 不批量刪除檔案或目錄。

## 相容性要求

- 既有 namespace 與 path 必須保留。
- 既有 HTTP method 必須保留。
- 既有 status code 與 response body 結構必須盡量保留。
- 登入 API 必須保留 `jwt` cookie 與 `Authorization` response header。
- JWT 驗證必須支援既有 cookie 流程；如原本支援 header，也必須保留。
- CORS 允許來源必須沿用 `appsettings.json`。
- SocketIO namespace 必須保留 `/message`、`/json_message`、`/broadcast_message`。

## 成功條件

- FastAPI app 可啟動並載入所有路由。
- `/docs` 與 `/openapi.json` 可開啟。
- 健康檢查、登入、whoami 與代表性業務 API 可正常回應。
- CORS preflight 行為符合既有設定。
- SocketIO 可透過 ASGI 連線。
- PyInstaller 打包後可執行並讀取設定檔。
