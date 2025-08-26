# app/utils/decorators.py
# アクセス制御用デコレータ

from functools import wraps
from flask import abort, session, redirect, url_for, flash
from app.models.user import User

def require_role(required_role):
    """
    指定された役割以上のユーザーのみアクセスを許可するデコレータ

    Args:
        required_role (str): 必要な役割 ('member', 'admin', 'developer')

    役割の階層:
    - developer: 最高権限（開発者）
    - admin: 管理者権限
    - member: 一般ユーザー
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # セッションベースの認証チェック
            user_id = session.get('user_id')
            if not user_id:
                flash('ログインが必要です', 'error')
                return redirect(url_for('auth.login'))

            # ユーザー情報を取得
            user = User.query.get(user_id)
            if not user:
                flash('無効なユーザーです', 'error')
                return redirect(url_for('auth.login'))

            # 役割の階層定義
            role_hierarchy = {
                'member': 1,
                'admin': 2,
                'developer': 3
            }

            user_role_level = role_hierarchy.get(user.role, 0)
            required_role_level = role_hierarchy.get(required_role, 999)

            if user_role_level < required_role_level:
                flash('アクセス権限がありません', 'error')
                return redirect(url_for('room.index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """管理者以上のアクセスが必要なデコレータ"""
    return require_role('admin')(f)

def developer_required(f):
    """開発者のみアクセス可能なデコレータ"""
    return require_role('developer')(f)
