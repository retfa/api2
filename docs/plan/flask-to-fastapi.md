# Flask 到 FastAPI 遷移實作計畫

## 階段一：建立 FastAPI 入口

- 將 `app.py` 改為建立 FastAPI app。
- 保留 PyInstaller frozen 與一般 Python 執行時的資料夾判斷。
- 將 `folders`、CORS origins、server host/port 等設定放入 `app.state` 或專案 runtime config。
- 設定 FastAPI `CORSMiddleware`，來源沿用 `appsettings.json`。

## 階段二：抽離 Flask 全域依賴

- 將 `current_app.config['folders']` 改為專案自有設定存取。
- 將 `Model.jwt_manager` 改為接收 request/config context。
- 將 `common.set_security` 改為不依賴 Flask app 物件。
- 保留既有 JWT payload 與簽章設定。

## 階段三：遷移 Controller

- 每個 `Controller/*.py` 改為 FastAPI `APIRouter`。
- `Namespace('name')` 對應為 `APIRouter(prefix='/name', tags=['name'])`。
- `Resource.get/post/put/patch/delete` 對應為 router method。
- Flask path 參數 `<string:id>` 改為 FastAPI `{id}`。
- `request.get_json()` 改為 FastAPI body 參數或 `await request.json()`。
- 回應需保留既有 dict、status code、cookie 與 header。

## 階段四：SocketIO ASGI 掛載

- 使用 `python-socketio` ASGI server。
- 保留既有 namespace 與事件名稱。
- 將 SocketIO app 與 FastAPI app 組合為同一 ASGI 入口。
- 驗證背景計時推播與 broadcast 行為。

## 階段五：文件、依賴與打包

- 更新 `requirements.txt`，加入 FastAPI 與 Uvicorn 相關依賴。
- 移除 Flask 相關依賴前，先確認所有 import 已替換。
- 更新 `app_D.spec` 與 `app_F.spec` hidden imports。
- 保留設定檔、模板與必要資料檔打包。

## 階段六：驗收

- 依 `docs/api-compatibility-checklist.md` 驗證。
- 執行 import 或 compile 檢查。
- 啟動本機服務確認主要端點與 SocketIO。
- 執行 PyInstaller 打包驗證。
