# 打包憲章

## 職責

PyInstaller spec 負責將 API、設定檔、模板與必要套件打包為可執行程式。

## 現有檔案

- `app_D.spec`
- `app_F.spec`
- `versioninfo.txt`

## 遷移規範

- FastAPI、Starlette、Uvicorn、Pydantic、python-socketio 的 hidden imports 需納入。
- `appsettings.json`、`connections.json`、`security.json` 必須納入 datas。
- `templates` 若仍被使用，必須納入 datas。
- 不得在打包設定中引用已移除的 Flask-only 模組。
- spec 更新後必須驗證打包產物可啟動並讀取設定檔。
