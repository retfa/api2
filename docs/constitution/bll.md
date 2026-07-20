# BLL 憲章

## 職責

BLL 負責商業邏輯與服務流程，不應依賴特定 Web framework。

## 遷移規範

- 不應使用 Flask `current_app`。
- 需要設定檔路徑時，應由參數、設定服務或 runtime config 提供。
- 不應直接處理 HTTP response、cookie 或 CORS。
- 保留既有商業邏輯與回傳資料語意。

## 相容性

BLL 方法簽名可為了移除 Flask 依賴而調整，但 Controller 必須維持外部 API 相容。
