# ユーザー認証関連のルーティング（URLとコントローラーの対応）をまとめたファイル
# Blueprintでルート定義し、コントローラー関数を呼び出す

from flask import Blueprint
from app.controllers import auth_controller

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_bp.route('/', methods=['GET', 'POST'])(auth_controller.index)
auth_bp.route('/login', methods=['GET', 'POST'])(auth_controller.login)
auth_bp.route('/logout')(auth_controller.logout)
auth_bp.route('/regist', methods=['GET', 'POST'])(auth_controller.regist)
auth_bp.route('/regist/confirm', methods=['POST'])(auth_controller.regist_confirm)
auth_bp.route('/regist/complete', methods=['GET'])(auth_controller.regist_complete)
