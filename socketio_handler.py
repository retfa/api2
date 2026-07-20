from flask import request
from flask_socketio import SocketIO, emit
import time

socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')  # 設置CORS允許所有來源

client_timers = {}


@socketio.on('connect', namespace='/message')
def message_connect():
    sid = request.sid  # 獲取客戶端的 session id
    print('Client connected to /message namespace')
    emit('response', {'data': 'First time connected'}, namespace='/message')

    # 每5秒向客戶端發送一次同步訊息
    def sync_time(sid):
        while True:
            start_time = time.time()
            socketio.emit('response', {'time': time.strftime('%Y-%m-%d %H:%M:%S')}, room=sid, namespace='/message')
            elapsed_time = time.time() - start_time
            socketio.sleep(max(0, 5 - elapsed_time))  # 確保每次迴圈間隔為5秒

    if sid not in client_timers:
        client_timers[sid] = socketio.start_background_task(sync_time, sid)


@socketio.on('disconnect', namespace='/message')
def message_disconnect():
    sid = request.sid  # 獲取客戶端的 session id
    print(f'Client {sid} disconnected from /message namespace')
    # 移除客戶端的計時器
    if sid in client_timers:
        del client_timers[sid]


@socketio.on('message', namespace='/message')
def message_message(data):
    print('Namespace /message received message: ' + data)
    random_number = int(data.split(': ')[1])  # 提取隨機數字
    if random_number >= 50:
        emit('response', {'data': 'OK'}, namespace='/message')
    else:
        emit('response', {'data': 'NG'}, namespace='/message')


# 定義第二個 WebSocket 事件處理器在 /json_message 命名空間
@socketio.on('connect', namespace='/json_message')
def json_message_connect():
    sid = request.sid  # 獲取客戶端的 session id
    print(f'Client {sid} connected to /json_message namespace')
    emit('response', {'data': 'First time connected'}, namespace='/json_message')


@socketio.on('disconnect', namespace='/json_message')
def json_message_disconnect():
    sid = request.sid  # 獲取客戶端的 session id
    print(f'Client {sid} disconnected from /json_message namespace')


@socketio.on('json_message', namespace='/json_message')
def json_message_json_message(data):
    print('Namespace /json_message received json message: ' + str(data))
    emit('response', {'data': 'JSON message received by /json_message namespace'})


# 定義第三個 WebSocket 事件處理器在 /broadcast_message 命名空間
@socketio.on('connect', namespace='/broadcast_message')
def broadcast_message_connect():
    sid = request.sid  # 獲取客戶端的 session id
    print(f'Client {sid} connected to /broadcast_message namespace')
    emit('response', {'data': 'First time connected'}, namespace='/broadcast_message')


@socketio.on('disconnect', namespace='/broadcast_message')
def broadcast_message_disconnect():
    sid = request.sid  # 獲取客戶端的 session id
    print(f'Client {sid} disconnected from /broadcast_message namespace')


@socketio.on('broadcast_message', namespace='/broadcast_message')
def broadcast_message_broadcast_message(data):
    print('Namespace /broadcast_message broadcasting message: ' + str(data))
    emit('response', {'data': 'Broadcast message received by /broadcast_message namespace'}, broadcast=True)



