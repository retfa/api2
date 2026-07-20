# 專案代理規範

本檔案定義 `C:\Project\@Web\Api2` 專案內所有代理與自動化工具必須遵守的操作規則。

## 文件語言與編碼

- 所有 Markdown 檔案必須使用繁體中文 `zh-TW` 撰寫。
- 所有 Markdown 檔案必須使用 `UTF-8` 編碼。
- 技術名詞、套件名稱、命令、路徑、API 名稱可保留英文原文。

## 刪除限制

禁止批量刪除文件或目錄。

不要使用：

- `del /s`
- `rd /s`
- `rmdir /s`
- `Remove-Item -Recurse`
- `rm -rf`

需要刪除文件時，只能一次刪除一個明確路徑的文件。

正確示範：

```powershell
Remove-Item "C:\path\to\file.txt"
```

如果需要批量刪除文件，應停止操作，並向使用者請求，讓使用者手動刪除。

## Flask 到 FastAPI 遷移規則

- 採完整替換策略：HTTP API 應改為 FastAPI 原生 `APIRouter`、`Request`、`Response`、`JSONResponse` 等介面。
- 必須保留既有公開 URL、HTTP method、status code、response body、cookie、header 與 CORS 行為。
- 不得只做表面啟動方式替換；需要移除 Flask 與 flask-restx 對路由層和全域設定的核心依賴。
- `current_app.config['folders']` 類型的設定依賴必須改為專案自有的 runtime config 或 FastAPI `app.state` 存取方式。
- SocketIO 需改為 ASGI 掛載，並保留既有 namespace 行為。
- 若仍維護 PyInstaller spec，需同步更新並確保打包後仍可讀取 `appsettings.json`、`connections.json`、`security.json` 與模板檔案；但 PyInstaller 不得取代 Docker container 作為正式部署方式。

## Docker Compose 部署原則

- 正式部署必須以 Docker container 執行 WebAPI。
- 所有正式部署服務必須透過 `docker compose` 管理。
- 禁止使用 `docker run` 作為正式部署方式。
- 禁止使用 PyInstaller 取代 container 作為正式部署方式。
- 服務應保持 stateless，不得依賴 container 本地狀態。
- 設定檔不得寫死在 image 中，應透過 bind mount 或環境變數提供。
- 敏感資訊不得寫死在 `docker-compose.yml`，必須透過 `.env` 或部署環境注入。
- DB data 必須使用 named volume 持久化。
- logs 必須寫入 volume 或 bind mount，不得只依賴 container 本地暫存空間。
- API 必須保留 `GET /health` 健康檢查端點。
- Docker Compose 完整架構標準詳見 `docs/constitution/docker-compose-constitution.md`；修改 Docker、部署、環境變數、service、volume、network 或 healthcheck 相關內容時，必須遵守該文件。

## Docker 相關修改規則

新增 service 時，必須同步檢查：

- `services/<name>/Dockerfile`
- `docker-compose.yml`
- network 設定
- volume 設定
- `.env.example` 或環境變數契約文件

修改 API 時：

- 不得破壞既有 `docker-compose.yml` 結構。
- 不得破壞 environment variable contract。
- 必須保留 `GET /health` endpoint。

修改 DB 時：

- 必須保留資料 volume。
- 不得破壞資料持久化。

## 實作原則

- 先讀取現有程式碼與設定，再修改。
- 優先保留現有業務邏輯，只替換 Web framework 邊界。
- 不做與遷移無關的重構、格式化或清理。
- 不批量刪除任何檔案、目錄、快取或產物。
