# app/utils/context_processors.py
# テンプレートで共通的に使用するコンテキストプロセッサー

from flask import session
from app.models.user import User

def user_context():
    """現在ログイン中のユーザー情報をテンプレートで利用できるようにする"""
    user_id = session.get('user_id')
    current_user = None
    username = session.get('username')
    is_logged_in = session.get('is_logged_in', False)

    if user_id:
        current_user = User.query.get(user_id)

    return {
        'current_user': current_user,
        'username': username,
        'is_logged_in': is_logged_in,
        'is_admin': current_user.role == 'admin' if current_user else False,
        'is_developer': current_user.role == 'developer' if current_user else False,
        'is_admin_or_developer': current_user.role in ['admin', 'developer'] if current_user else False
    }
