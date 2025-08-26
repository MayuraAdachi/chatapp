# app/__init__.py
# 初期化や設定を行う
import os
from flask import Flask
from dotenv import load_dotenv
from app.config import const
from .extensions import db, socketio
from app.routes.room_routes import room_bp
from app.routes.auth_routes import auth_bp

# Flaskのセットアップ
def create_app():
    # .envファイルから環境変数を読み込む
    load_dotenv()

    # Flaskアプリケーションのインスタンスを作成
    app = Flask(__name__)

    # Flaskの設定
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # アプリ名・バージョン・デバッグモードの設定
    app.config['APP_TITLE'] = const.APP_TITLE
    app.config['VERSION'] = const.VERSION
    app.config['DEBUG_MODE'] = os.getenv('DEBUG_MODE', 'False').lower() in ['true', '1', 'yes']
    app.debug = app.config['DEBUG_MODE']
    # チャットログの保存日数（通常・バックアップ）の設定
    app.config['CHAT_LOG_DAYS'] = int(const.CHAT_LOG_DAYS)
    app.config['CHAT_BACKUP_DAYS'] = int(const.CHAT_BACKUP_DAYS)

    # SQLAlchemy、SocketIOをFlaskアプリに紐付け
    db.init_app(app)
    socketio.init_app(app)

    # Blueprintを登録
    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)

    return app
