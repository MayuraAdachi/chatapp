# run.py
# Flaskアプリケーションを起動する
from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    debug_mode = app.config.get('DEBUG_MODE', False)
    socketio.run(app, debug=debug_mode)
