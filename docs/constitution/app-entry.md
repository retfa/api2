# App 入口憲章

## 職責

`app.py` 是應用程式入口，負責建立 FastAPI app、載入設定、設定 middleware、註冊 router、掛載 SocketIO 與提供執行入口。

## 規範

- 必須保留 PyInstaller frozen 與一般 Python 執行時的 folder 判斷。
- `appsettings.json` 必須從 exe folder 讀取。
- `security.json` 與其他打包資料必須支援 temproot folder。
- CORS 必須沿用 `appsettings.json`。
- 不應在 import 階段直接啟動 server。

## FastAPI 實作要求

- FastAPI app object 應命名為 `app`。
- Runtime 設定應放在 `app.state` 或專案自有設定物件。
- 本機執行可使用 Uvicorn，host/port 以設定檔為準。
