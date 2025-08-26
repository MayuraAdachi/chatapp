# app/services/admin_service.py
"""
管理者・開発者関連のビジネスロジックを提供するサービス層
"""
from flask import session, flash
from functools import wraps
from sqlalchemy import text, func
from app.models.user import User
from app.models.room import Room
from app.models.message import Message
from app.extensions import db
from werkzeug.security import generate_password_hash
import os
from datetime import datetime, timedelta


class AdminService:
    """管理者・開発者サービス"""

    @staticmethod
    def require_admin_or_developer(f):
        """管理者または開発者権限が必要なルートをデコレート"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                flash('ログインが必要です', 'error')
                return False, 'login_required'

            user = User.query.get(user_id)
            if not user or user.role not in ['admin', 'developer']:
                flash('管理者権限が必要です', 'error')
                return False, 'permission_denied'

            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def require_admin(f):
        """管理者権限が必要なルートをデコレート"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                flash('ログインが必要です', 'error')
                return False, 'login_required'

            user = User.query.get(user_id)
            if not user or user.role != 'admin':
                flash('管理者権限が必要です', 'error')
                return False, 'permission_denied'

            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def get_dashboard_stats():
        """ダッシュボード用の統計情報を取得"""
        try:
            total_users = User.query.count()

            try:
                total_rooms = Room.query.count()
            except Exception:
                total_rooms = 0

            try:
                total_messages = db.session.execute(text('SELECT COUNT(*) FROM messages')).scalar()
            except Exception:
                total_messages = 0

            admin_users = User.query.filter_by(role='admin').count()
            developer_users = User.query.filter_by(role='developer').count()
            member_users = User.query.filter_by(role='member').count()

            return {
                'total_users': total_users,
                'total_rooms': total_rooms,
                'total_messages': total_messages,
                'admin_users': admin_users,
                'developer_users': developer_users,
                'member_users': member_users
            }
        except Exception as e:
            return {
                'total_users': 0,
                'total_rooms': 0,
                'total_messages': 0,
                'admin_users': 0,
                'developer_users': 0,
                'member_users': 0
            }

    @staticmethod
    def get_system_logs(limit=50):
        """システムログを取得"""
        try:
            log_file = os.path.join('logs', 'app.log')
            if not os.path.exists(log_file):
                return []

            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return [line.strip() for line in lines[-limit:]]
        except Exception as e:
            return [f"ログ読み取りエラー: {str(e)}"]

    @staticmethod
    def get_recent_activities(limit=20):
        """最近のアクティビティを取得"""
        try:
            recent_messages = db.session.query(Message)\
                .filter(Message.message_type == 'system')\
                .order_by(Message.created_at.desc())\
                .limit(limit)\
                .all()

            activities = []
            for msg in recent_messages:
                activities.append({
                    'timestamp': msg.created_at,
                    'content': msg.content,
                    'room_name': msg.room.name if msg.room else '不明',
                    'display_name': msg.display_name
                })

            return activities
        except Exception as e:
            return []

    @staticmethod
    def get_user_statistics():
        """ユーザー統計を取得"""
        try:
            total_users = db.session.query(User).count()
            online_users = db.session.query(User)\
                .filter(User.status == 'online').count()
            admin_users = db.session.query(User)\
                .filter(User.role.in_(['admin', 'developer'])).count()

            week_ago = datetime.now() - timedelta(days=7)
            new_users_week = db.session.query(User)\
                .filter(User.created_at >= week_ago).count()

            return {
                'total': total_users,
                'online': online_users,
                'admins': admin_users,
                'new_this_week': new_users_week
            }
        except Exception as e:
            return {
                'total': 0,
                'online': 0,
                'admins': 0,
                'new_this_week': 0
            }

    @staticmethod
    def get_room_statistics():
        """ルーム統計を取得"""
        try:
            total_rooms = db.session.query(Room).count()
            public_rooms = db.session.query(Room)\
                .filter(Room.is_private == False).count()
            private_rooms = db.session.query(Room)\
                .filter(Room.is_private == True).count()

            active_rooms = db.session.query(
                Room.name,
                func.count(Message.id).label('message_count')
            )\
            .join(Message, Room.id == Message.room_id)\
            .group_by(Room.id, Room.name)\
            .order_by(func.count(Message.id).desc())\
            .limit(5)\
            .all()

            return {
                'total': total_rooms,
                'public': public_rooms,
                'private': private_rooms,
                'most_active': [{'name': room.name, 'messages': room.message_count}
                              for room in active_rooms]
            }
        except Exception as e:
            return {
                'total': 0,
                'public': 0,
                'private': 0,
                'most_active': []
            }

    @staticmethod
    def get_message_statistics():
        """メッセージ統計を取得"""
        try:
            total_messages = db.session.query(Message).count()

            today = datetime.now().date()
            today_messages = db.session.query(Message)\
                .filter(func.date(Message.created_at) == today).count()

            week_ago = datetime.now() - timedelta(days=7)
            week_messages = db.session.query(Message)\
                .filter(Message.created_at >= week_ago).count()

            return {
                'total': total_messages,
                'today': today_messages,
                'this_week': week_messages
            }
        except Exception as e:
            return {
                'total': 0,
                'today': 0,
                'this_week': 0
            }

    @staticmethod
    def get_users_paginated(page=1, per_page=20):
        """ページング付きユーザー一覧を取得"""
        return User.query.paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def update_user_role(user_id, new_role):
        """ユーザーロール変更"""
        if new_role not in ['admin', 'developer', 'member']:
            return False, '無効なロールです'

        user = User.query.get(user_id)
        if not user:
            return False, 'ユーザーが見つかりません'

        try:
            user.role = new_role
            db.session.commit()
            return True, f'{user.username}のロールを{new_role}に変更しました'
        except Exception as e:
            db.session.rollback()
            return False, 'ロール変更に失敗しました'

    @staticmethod
    def reset_user_password(username, new_password):
        """パスワードリセット"""
        if not username or not new_password:
            return False, 'ユーザー名とパスワードを入力してください'

        user = User.query.filter_by(username=username).first()
        if not user:
            return False, 'ユーザーが見つかりません'

        try:
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            return True, f'{username}のパスワードをリセットしました'
        except Exception as e:
            db.session.rollback()
            return False, 'パスワードリセットに失敗しました'

    @staticmethod
    def get_user_and_permissions(user_id):
        """ユーザー情報と権限を取得"""
        user = User.query.get(user_id)
        if not user:
            return None, False, False

        is_admin = user.role == 'admin'
        is_developer = user.role == 'developer'

        return user, is_admin, is_developer

    @staticmethod
    def check_admin_or_developer_permission(user_id):
        """管理者または開発者権限をチェック"""
        if not user_id:
            return False, 'ログインが必要です'

        user = User.query.get(user_id)
        if not user or user.role not in ['admin', 'developer']:
            return False, '管理者権限が必要です'

        return True, None

    @staticmethod
    def check_admin_permission(user_id):
        """管理者権限をチェック"""
        if not user_id:
            return False, 'ログインが必要です'

        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return False, '管理者権限が必要です'

        return True, None

    @staticmethod
    def get_user_statistics():
        """ユーザー統計を取得"""
        try:
            total_users = db.session.query(User).count()
            online_users = db.session.query(User)\
                .filter(User.status == 'online').count()
            admin_users = db.session.query(User)\
                .filter(User.role.in_(['admin', 'developer'])).count()

            week_ago = datetime.now() - timedelta(days=7)
            new_users_week = db.session.query(User)\
                .filter(User.created_at >= week_ago).count()

            return {
                'total': total_users,
                'online': online_users,
                'admins': admin_users,
                'new_this_week': new_users_week
            }
        except Exception as e:
            return {
                'total': 0,
                'online': 0,
                'admins': 0,
                'new_this_week': 0
            }

    @staticmethod
    def get_room_statistics():
        """ルーム統計を取得"""
        try:
            total_rooms = db.session.query(Room).count()
            public_rooms = db.session.query(Room)\
                .filter(Room.is_private == False).count()
            private_rooms = db.session.query(Room)\
                .filter(Room.is_private == True).count()

            active_rooms = db.session.query(
                Room.name,
                func.count(Message.id).label('message_count')
            )\
            .join(Message, Room.id == Message.room_id)\
            .group_by(Room.id, Room.name)\
            .order_by(func.count(Message.id).desc())\
            .limit(5)\
            .all()

            return {
                'total': total_rooms,
                'public': public_rooms,
                'private': private_rooms,
                'most_active': [{'name': room.name, 'messages': room.message_count}
                              for room in active_rooms]
            }
        except Exception as e:
            return {
                'total': 0,
                'public': 0,
                'private': 0,
                'most_active': []
            }
