# 一般ユーザー向け公開機能のルーティング

from flask import Blueprint, render_template, session, redirect, url_for
from app.controllers import room_controller
from app.extensions import csrf

# =============================================================================
# メインページ・トップレベル
# =============================================================================
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """トップページの表示（ログイン済みの場合はroom.indexにリダイレクト）"""
    from app.services.room_service import RoomService

    # セッションを初期化（必要に応じてuser_idを生成）
    RoomService.set_user_session()

    # ログイン状態をチェック
    user_id = session.get('user_id')
    is_logged_in = session.get('is_logged_in', False)
    username = session.get('username')

    # セッションの整合性をチェック
    # ログインしていないのにユーザー名だけある場合は無効なセッションとして扱う
    if not is_logged_in and username and 'user_id' in session:
        # 匿名ユーザーとしてのセッションが残っている場合は継続
        pass
    elif not is_logged_in and username:
        # 不整合なセッション状態をクリア
        session.pop('username', None)
        username = None

    # ログイン済みユーザーまたは匿名ユーザーで一度参加済みの場合はルーム一覧にリダイレクト
    if (user_id and is_logged_in) or (user_id and username):
        return redirect(url_for('room.index'))

    # 初回アクセスの場合はトップページを表示
    return render_template('index.html')

# =============================================================================
# チャットルーム関連（一般ユーザー機能）
# =============================================================================
room_bp = Blueprint('room', __name__, url_prefix='/room')

# ユーザー識別用のセッションIDをセット
room_bp.before_app_request(room_controller.set_user)
room_bp.route('/', methods=['GET', 'POST'])(room_controller.index)
room_bp.route('/create', methods=['GET', 'POST'])(room_controller.room_create)
room_bp.route('/validate_room_create_form', methods=['POST'])(room_controller.validate_room_create_form)
room_bp.route('/delete/<room_id>', methods=['POST'])(room_controller.delete_room)
room_bp.route('/chat/<room_name>', methods=['GET'])(room_controller.chat)
room_bp.route('/join', methods=['POST'])(room_controller.join_room)


def update_room_settings():
    """
    ルーム設定変更（Ajax用）
    """
    from flask import request, jsonify
    data = request.get_json()
    room_id = data.get('room_id')
    name = data.get('name')
    description = data.get('description')
    max_members = data.get('max_members')
    password = data.get('password')
    # ここで権限・バリデーション・DB更新処理
    # RoomService.update_room_settings(room_id, ...) など
    # 仮実装（成功のみ返す）
    return jsonify({ 'success': True })

room_bp.route('/update_settings', methods=['POST'])(update_room_settings)
# =============================================================================
# 公開Blueprint一覧
# =============================================================================
public_blueprints = [main_bp, room_bp]
