# run.py
# Flaskアプリケーションを起動する
import eventlet
eventlet.monkey_patch()
from app import create_app
from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    # アプリケーション設定からデバッグモードを取得
    debug_mode = app.debug
    print(f"Starting app with debug_mode = {debug_mode}")

    socketio.run(app, debug=debug_mode)
    # app.run(debug=debug_mode)  # 通常のFlaskで起動
