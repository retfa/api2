# Api2 MES API

本專案是 MES 相關 Web API，目前入口為 Flask 與 flask-restx 架構，後續將完整遷移為 FastAPI。遷移期間以保留既有 API 行為為最高優先：URL、HTTP method、回應格式、JWT cookie/header、CORS 與打包方式都必須維持相容。

## 目前狀態

- 目前主要入口：`app.py`
- 目前路由來源：`Controller/*.py`
- 目前 API 文件：flask-restx `/swagger`
- 目前設定檔：
  - `appsettings.json`
  - `connections.json`
  - `security.json`
- 目前打包設定：
  - `app_D.spec`
  - `app_F.spec`

## 遷移目標

遷移完成後，專案應使用 FastAPI 作為 HTTP API framework，並使用 ASGI 方式同時承載 HTTP API 與 SocketIO。

預期啟動方式：

```powershell
uvicorn app:app --host 0.0.0.0 --port 5000
```

實際 host 與 port 應以 `appsettings.json` 的 `Server.Host` 與 `Server.Port` 為準。

## API 文件

FastAPI 遷移完成後，API 文件位置改為：

- Swagger UI：`/docs`
- OpenAPI JSON：`/openapi.json`

若既有系統仍依賴 `/swagger`，可在實作時加入相容 redirect 或相容路由。

## 設定檔

`appsettings.json` 用於伺服器、JWT 到期時間與 CORS 設定。

`connections.json` 用於資料庫連線字串。

`security.json` 用於 JWT key、issuer、audience 等安全設定。

FastAPI 遷移時不得讓 BLL、DAL、Model 直接依賴 Flask `current_app`；應改由專案自有設定服務或 FastAPI `app.state` 提供。

## 文件索引

- `AGENTS.md`：專案代理與操作規範
- `docs/spec/flask-to-fastapi.md`：遷移需求規格
- `docs/plan/flask-to-fastapi.md`：遷移實作計畫
- `docs/tasks/flask-to-fastapi.md`：遷移任務清單
- `docs/api-compatibility-checklist.md`：API 相容性驗收清單
- `docs/constitution/*.md`：各模組架構規範
