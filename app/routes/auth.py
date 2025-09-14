# 認証・ユーザー管理関連のルーティング

from flask import Blueprint
from app.controllers import auth_controller

# =============================================================================
# 認証関連ルート (/auth)
# =============================================================================
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 基本認証機能
auth_bp.route('/', methods=['GET'])(auth_controller.index)
auth_bp.route('/login', methods=['GET', 'POST'])(auth_controller.login)
auth_bp.route('/logout')(auth_controller.logout)

# ユーザー登録
auth_bp.route('/regist', methods=['GET', 'POST'])(auth_controller.regist)
auth_bp.route('/regist/confirm', methods=['GET', 'POST'])(auth_controller.regist_confirm)
auth_bp.route('/regist/complete', methods=['GET', 'POST'])(auth_controller.regist_complete)

# ユーザー設定・プロフィール
auth_bp.route('/settings', methods=['GET', 'POST'])(auth_controller.settings)
auth_bp.route('/change_password', methods=['POST'])(auth_controller.change_password)

# =============================================================================
# 認証Blueprint一覧
# =============================================================================
auth_blueprints = [auth_bp]
