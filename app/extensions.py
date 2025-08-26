# app/extensions.py
# Flask拡張機能（SocketIOやSQLAlchemyなど）のインスタンス生成をまとめるファイル

from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# SocketIOインスタンスを生成（アプリ本体とは分離）
socketio = SocketIO()  # async_mode指定なし

# SQLAlchemyインスタンスを生成
# （Flaskアプリ本体でinit_appすることで利用可能）
db = SQLAlchemy()

# CSRF保護インスタンスを生成
csrf = CSRFProtect()

# Babel インスタンスを生成（多言語対応）- Flask-Babelがインストールされている場合のみ
babel = None
try:
    from flask_babel import Babel
    babel = Babel()
except ImportError:
    print("Flask-Babel not installed. Multilingual support disabled.")
    babel = None
