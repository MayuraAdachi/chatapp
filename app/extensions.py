# app/extensions.py
# Flask拡張機能（SocketIOやSQLAlchemyなど）のインスタンス生成をまとめるファイル

from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# SocketIOインスタンスを生成（アプリ本体とは分離）
socketio = SocketIO()

# SQLAlchemyインスタンスを生成
# （Flaskアプリ本体でinit_appすることで利用可能）
db = SQLAlchemy()
