# Flask 到 FastAPI 遷移任務清單

## 文件準備

- [x] 建立 `AGENTS.md`
- [x] 建立 `README.md`
- [x] 建立需求規格、實作計畫與任務清單
- [x] 建立模組憲章文件
- [x] 建立 API 相容性驗收清單

## App 入口

- [ ] 將 `app.py` 改為 FastAPI app。
- [ ] 實作 PyInstaller-aware folder 初始化。
- [ ] 將設定放入 `app.state` 或專案 runtime config。
- [ ] 設定 FastAPI CORS middleware。
- [ ] 保留 `/download-pdf`。
- [ ] 保留 `/swagger-ui-with-download` 或改為相容實作。

## Controller 遷移

- [ ] 建立 FastAPI router 註冊機制。
- [ ] 遷移 `authentication` controller。
- [ ] 遷移 `healthcheck` controller。
- [ ] 遷移 `user` controller。
- [ ] 遷移 `permission` controller。
- [ ] 遷移其餘 Controller。
- [ ] 保留既有 URL、method、status code 與 response body。

## Config 與 JWT

- [ ] 移除 BLL/DAL/Model 對 Flask `current_app` 的依賴。
- [ ] 改寫 `JwtManager`。
- [ ] 保留 JWT cookie 與 Authorization header 行為。
- [ ] 保留 `security.json` 與 `appsettings.json` 設定來源。

## SocketIO

- [ ] 將 Flask-SocketIO 改為 `python-socketio` ASGI。
- [ ] 保留 `/message` namespace。
- [ ] 保留 `/json_message` namespace。
- [ ] 保留 `/broadcast_message` namespace。
- [ ] 驗證背景推播與 broadcast。

## 依賴與打包

- [ ] 更新 `requirements.txt`。
- [ ] 更新 `app_D.spec`。
- [ ] 更新 `app_F.spec`.
- [ ] 驗證 PyInstaller 打包後可讀取設定檔。

## 驗收

- [ ] 啟動 FastAPI 服務。
- [ ] 驗證 `/docs`。
- [ ] 驗證 `/openapi.json`。
- [ ] 驗證登入、whoami、healthcheck。
- [ ] 驗證 CORS preflight。
- [ ] 驗證 SocketIO。
- [ ] 執行 compile 或 import 檢查。
