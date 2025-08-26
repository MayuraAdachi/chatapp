#!/usr/bin/env python3
"""
初期データ投入スクリプト
Werkzeugと互換性のあるパスワードハッシュで初期ユーザーを作成
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.room import Room
from app.models.room_member import RoomMember
from app.models.message import Message
from app.models.session import Session
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone

def clear_existing_data():
    """既存データを削除"""
    print("データ削除中...")
    # 外部キー制約に配慮した順序で削除
    db.session.execute(db.text("DELETE FROM messages"))
    db.session.execute(db.text("DELETE FROM room_members"))
    db.session.execute(db.text("DELETE FROM rooms"))
    db.session.execute(db.text("DELETE FROM sessions"))
    db.session.execute(db.text("DELETE FROM users"))
    db.session.commit()
    print("削除完了")

def create_initial_users():
    """初期ユーザーを作成"""
    print("ユーザー作成中...")

    users_data = [
        # 管理者ユーザー
        {
            'username': 'admin',
            'email': 'admin@chatapp.local',
            'password': 'admin123',
            'display_name': '管理者',
            'role': 'admin',
            'status': 'online',
            'bio': 'システム管理者です。何かお困りのことがあればお声かけください。'
        },
        {
            'username': 'sub_admin',
            'email': 'sub_admin@chatapp.local',
            'password': 'sub_admin123',
            'display_name': '副管理者',
            'role': 'admin',
            'status': 'offline',
            'bio': '副管理者として運営をサポートしています。'
        },
        # 開発者ユーザー
        {
            'username': 'dev1',
            'email': 'dev1@chatapp.local',
            'password': 'dev123',
            'display_name': '開発者1',
            'role': 'developer',
            'status': 'away',
            'bio': 'フルスタック開発者。'
        },
        {
            'username': 'dev2',
            'email': 'dev2@chatapp.local',
            'password': 'dev123',
            'display_name': '開発者2',
            'role': 'developer',
            'status': 'offline',
            'bio': 'フルスタック開発者。'
        },
        {
            'username': 'dev3',
            'email': 'dev3@chatapp.local',
            'password': 'dev123',
            'display_name': '開発者3',
            'role': 'developer',
            'status': 'online',
            'bio': 'フルスタック開発者。'
        },
        # テストユーザー
        {
            'username': 'test001',
            'email': 'test001@chatapp.local',
            'password': 'test123',
            'display_name': 'テストユーザー001',
            'role': 'member',
            'status': 'online',
            'status_message': 'テスト中です'
        },
        {
            'username': 'test002',
            'email': 'test002@chatapp.local',
            'password': 'test123',
            'display_name': 'テストユーザー002',
            'role': 'member',
            'status': 'away',
            'status_message': '離席中'
        },
        {
            'username': 'test003',
            'email': 'test003@chatapp.local',
            'password': 'test123',
            'display_name': 'テストユーザー003',
            'role': 'member',
            'status': 'busy',
            'status_message': '作業中'
        },
        {
            'username': 'test004',
            'email': 'test004@chatapp.local',
            'password': 'test123',
            'display_name': 'テストユーザー004',
            'role': 'member',
            'status': 'offline',
            'status_message': ''
        },
        {
            'username': 'test005',
            'email': 'test005@chatapp.local',
            'password': 'test123',
            'display_name': 'テストユーザー005',
            'role': 'member',
            'status': 'invisible',
            'status_message': 'ステルスモード'
        }
    ]

    for user_data in users_data:
        password = user_data.pop('password')
        user = User(
            password_hash=generate_password_hash(password),
            **user_data
        )
        db.session.add(user)
        print(f"{user.username}")

    db.session.commit()
    print("作成完了")

def create_initial_rooms():
    """初期ルームを作成"""
    print("ルーム作成中...")

    # 管理者ユーザーを取得
    admin = User.query.filter_by(username='admin').first()
    dev1 = User.query.filter_by(username='dev1').first()

    # 匿名セッションを取得
    anon_session = Session.query.filter_by(id='anon_session_001').first()

    rooms_data = [
        {
            'name': '全体チャット',
            'description': '全員が参加できる全体チャットルームです',
            'type': 'group',
            'is_private': False,
            'created_by_user_id': admin.id,
            'created_by_name': admin.username,
            'max_members': 100
        },
        {
            'name': '開発者用',
            'description': '開発者専用のチャットルームです',
            'type': 'group',
            'is_private': True,
            'created_by_user_id': dev1.id,
            'created_by_name': dev1.username,
            'max_members': 10
        },
        {
            'name': 'テスト用',
            'description': 'テスト用のチャットルームです',
            'type': 'group',
            'is_private': False,
            'created_by_user_id': admin.id,
            'created_by_name': admin.username,
            'max_members': 50
        },
        {
            'name': '匿名交流ルーム',
            'description': '匿名ユーザーが作成したルームです',
            'type': 'group',
            'is_private': False,
            'created_by_session': anon_session.id if anon_session else None,
            'created_by_name': anon_session.display_name if anon_session else '匿名ユーザー',
            'max_members': 30
        }
    ]

    created_rooms = []
    for room_data in rooms_data:
        room = Room(**room_data)
        db.session.add(room)
        created_rooms.append(room)
        print(f"{room.name}")

    db.session.commit()
    return created_rooms

def create_room_members(rooms):
    """ルームメンバーを作成"""
    print("メンバー追加中...")

    users = User.query.all()

    # 全体チャットには全員参加
    general_room = rooms[0]
    for user in users:
        role = 'creator' if user.username == 'admin' else 'member'
        member = RoomMember(
            room_id=general_room.id,
            user_id=user.id,
            display_name=user.display_name,
            role=role
        )
        db.session.add(member)

    # 開発者用ルームには開発者と管理者のみ
    dev_room = rooms[1]
    dev_users = User.query.filter(User.role.in_(['developer', 'admin'])).all()
    for user in dev_users:
        role = 'creator' if user.username == 'dev1' else 'admin' if user.role == 'admin' else 'member'
        member = RoomMember(
            room_id=dev_room.id,
            user_id=user.id,
            display_name=user.display_name,
            role=role
        )
        db.session.add(member)

    # テスト用ルームにはテストユーザーと管理者
    test_room = rooms[2]
    test_users = User.query.filter(User.username.like('test%')).all()
    admin = User.query.filter_by(username='admin').first()
    all_test_users = test_users + [admin]
    for user in all_test_users:
        role = 'creator' if user.username == 'admin' else 'member'
        member = RoomMember(
            room_id=test_room.id,
            user_id=user.id,
            display_name=user.display_name,
            role=role
        )
        db.session.add(member)

    # 匿名交流ルームには一般ユーザーと匿名ユーザー
    if len(rooms) > 3:  # 匿名交流ルームが存在する場合
        anon_room = rooms[3]
        anon_session = Session.query.filter_by(id='anon_session_001').first()

        # 匿名ユーザー（作成者）を追加
        if anon_session:
            anon_member = RoomMember(
                room_id=anon_room.id,
                session_id=anon_session.id,
                display_name=anon_session.display_name,
                role='creator'
            )
            db.session.add(anon_member)

        # 一般ユーザーを数人追加
        general_users = User.query.filter(User.username.in_(['test001', 'test002', 'test003'])).all()
        for user in general_users:
            member = RoomMember(
                room_id=anon_room.id,
                user_id=user.id,
                display_name=user.display_name,
                role='member'
            )
            db.session.add(member)

    db.session.commit()

def create_sample_messages(rooms):
    """サンプルメッセージを作成"""
    print("メッセージ作成中...")

    admin = User.query.filter_by(username='admin').first()
    dev1 = User.query.filter_by(username='dev1').first()
    test001 = User.query.filter_by(username='test001').first()

    # 全体チャットのメッセージ
    general_room = rooms[0]
    messages = [
        {
            'room_id': general_room.id,
            'user_id': admin.id,
            'display_name': admin.display_name,
            'content': 'チャットアプリへようこそ！',
            'message_type': 'system'
        },
        {
            'room_id': general_room.id,
            'user_id': dev1.id,
            'display_name': dev1.display_name,
            'content': 'よろしくお願いします！',
            'message_type': 'text'
        },
        {
            'room_id': general_room.id,
            'user_id': test001.id,
            'display_name': test001.display_name,
            'content': 'テストメッセージです',
            'message_type': 'text'
        }
    ]

    # 開発者用ルームのメッセージ
    dev_room = rooms[1]
    dev_messages = [
        {
            'room_id': dev_room.id,
            'user_id': dev1.id,
            'display_name': dev1.display_name,
            'content': '開発者ルームが作成されました',
            'message_type': 'system'
        },
        {
            'room_id': dev_room.id,
            'user_id': admin.id,
            'display_name': admin.display_name,
            'content': '開発お疲れさまです',
            'message_type': 'text'
        }
    ]

    # 匿名交流ルームのメッセージ
    anon_messages = []
    if len(rooms) > 3:  # 匿名交流ルームが存在する場合
        anon_room = rooms[3]
        anon_session = Session.query.filter_by(id='anon_session_001').first()

        if anon_session:
            anon_messages = [
                {
                    'room_id': anon_room.id,
                    'session_id': anon_session.id,
                    'display_name': anon_session.display_name,
                    'content': 'こんにちは！匿名交流ルームを作成しました',
                    'message_type': 'text'
                },
                {
                    'room_id': anon_room.id,
                    'user_id': test001.id,
                    'display_name': test001.display_name,
                    'content': 'よろしくお願いします！',
                    'message_type': 'text'
                }
            ]

    all_messages = messages + dev_messages + anon_messages
    for msg_data in all_messages:
        message = Message(**msg_data)
        db.session.add(message)

    db.session.commit()

def create_anonymous_sessions():
    """匿名ユーザーのセッションを作成"""
    print("匿名セッション作成中...")

    sessions_data = [
        {
            'id': 'anon_session_001',
            'display_name': '匿名太郎',
            'expires_at': datetime.now(timezone.utc) + timedelta(hours=24)
        },
        {
            'id': 'anon_session_002',
            'display_name': '匿名花子',
            'expires_at': datetime.now(timezone.utc) + timedelta(hours=24)
        }
    ]

    created_sessions = []
    for session_data in sessions_data:
        session = Session(**session_data)
        db.session.add(session)
        created_sessions.append(session)
        print(f"{session.display_name}")

    db.session.commit()
    return created_sessions

def main():
    """メイン処理"""
    app = create_app()

    with app.app_context():
        try:
            # 既存データを削除
            clear_existing_data()

            # 初期ユーザーを作成
            create_initial_users()

            # 匿名ユーザーのセッションを作成
            create_anonymous_sessions()

            # 初期ルームを作成
            rooms = create_initial_rooms()

            # ルームメンバーを作成
            create_room_members(rooms)

            # サンプルメッセージを作成
            create_sample_messages(rooms)

            print("\n完了")

        except Exception as e:
            print(f"エラー: {e}")
            db.session.rollback()
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
