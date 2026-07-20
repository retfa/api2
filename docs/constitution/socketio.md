# SocketIO 憲章

## 職責

SocketIO 提供即時訊息、JSON 訊息與 broadcast 功能。

## Namespace

必須保留以下 namespace：

- `/message`
- `/json_message`
- `/broadcast_message`

## 遷移規範

- Flask-SocketIO 應改為 `python-socketio` ASGI server。
- SocketIO app 必須與 FastAPI app 一起由 ASGI server 承載。
- 事件名稱與 payload 結構應保留。
- `/message` 的背景時間推播行為應保留。

## 驗收

每個 namespace 都必須能 connect、disconnect，並處理既有事件。
