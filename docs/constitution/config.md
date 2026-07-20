# Config 憲章

## 職責

設定系統負責提供 app、資料庫、安全與 CORS 設定。

## 設定檔

- `appsettings.json`：server、JWT expiration、database host、CORS。
- `connections.json`：資料庫連線設定。
- `security.json`：JWT key、issuer、audience。

## 遷移規範

- 必須支援 PyInstaller frozen 環境。
- 必須支援一般 Python script 環境。
- 不得讓 BLL/DAL/Model 直接讀取 FastAPI app 物件。
- 可建立專案自有 runtime config helper，集中管理 folder 與設定檔路徑。

## CORS

CORS origins 必須沿用 `appsettings.json`，不得硬編碼覆蓋。
