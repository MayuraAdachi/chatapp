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
    db.session.execute(db.text("DELETE FROM t_messages"))
    db.session.execute(db.text("DELETE FROM t_room_members"))
    db.session.execute(db.text("DELETE FROM t_rooms"))
    db.session.execute(db.text("DELETE FROM t_sessions"))
    db.session.execute(db.text("DELETE FROM t_users"))

    db.session.execute(db.text("DELETE FROM m_user_roles WHERE is_system = FALSE"))
    db.session.execute(db.text("DELETE FROM m_user_statuses WHERE is_system = FALSE"))
    db.session.execute(db.text("DELETE FROM m_room_types WHERE is_system = FALSE"))
    db.session.execute(db.text("DELETE FROM m_message_types WHERE is_system = FALSE"))
    db.session.execute(db.text("DELETE FROM m_room_roles WHERE is_system = FALSE"))
    db.session.execute(db.text("DELETE FROM m_languages WHERE is_system = FALSE"))

    db.session.commit()
    print("削除完了")

def create_initial_users():
    """初期ユーザーを作成"""
    print("ユーザー作成中...")

    users_data = [
        # 管理者
        {
            'username': 'admin',
            'email': 'admin@chatapp.local',
            'password': 'admin123',
            'display_name': '管理者',
            'role': 'admin',
            'status': 'online',
            'bio': '全マスタ・全ユーザー管理可能な管理者です。'
        },
        # 開発者
        {
            'username': 'dev1',
            'email': 'dev1@chatapp.local',
            'password': 'dev123',
            'display_name': '開発者1',
            'role': 'developer',
            'status': 'away',
            'bio': '開発・運用全般を担当しています。'
        },
        # 副管理者
        {
            'username': 'subadmin',
            'email': 'subadmin@chatapp.local',
            'password': 'subadmin123',
            'display_name': '副管理者',
            'role': 'sub_admin',
            'status': 'offline',
            'bio': '特定マスタ・ユーザー管理が可能な副管理者です。'
        },
        # モデレーター
        {
            'username': 'mod1',
            'email': 'mod1@chatapp.local',
            'password': 'mod123',
            'display_name': 'モデレーター1',
            'role': 'moderator',
            'status': 'busy',
            'bio': '特定マスタの閲覧・ユーザー情報の確認が可能です。'
        },
        # メンバー
        {
            'username': 'member1',
            'email': 'member1@chatapp.local',
            'password': 'member123',
            'display_name': 'メンバー1',
            'role': 'member',
            'status': 'online',
            'status_message': 'チャットを楽しんでいます！'
        },
        {
            'username': 'member2',
            'email': 'member2@chatapp.local',
            'password': 'member123',
            'display_name': 'メンバー2',
            'role': 'member',
            'status': 'away',
            'status_message': '少し離席中です'
        },
        {
            'username': 'member3',
            'email': 'member3@chatapp.local',
            'password': 'member123',
            'display_name': 'メンバー3',
            'role': 'member',
            'status': 'busy',
            'status_message': '作業中'
        },
        {
            'username': 'member4',
            'email': 'member4@chatapp.local',
            'password': 'member123',
            'display_name': 'メンバー4',
            'role': 'member',
            'status': 'offline',
            'status_message': ''
        },
        {
            'username': 'member5',
            'email': 'member5@chatapp.local',
            'password': 'member123',
            'display_name': 'メンバー5',
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

    db.session.commit()
    return created_rooms

def room_create_members(rooms):
    """ルームメンバーを作成"""
    print("メンバー追加中...")

    users = User.query.all()

    # 全体チャットには全員参加
    general_room = rooms[0]
    for user in users:
        role = 'owner' if user.username == 'admin' else 'member'
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
        role = 'owner' if user.username == 'dev1' else 'admin' if user.role == 'admin' else 'member'
        member = RoomMember(
            room_id=dev_room.id,
            user_id=user.id,
            display_name=user.display_name,
            role=role
        )
        db.session.add(member)

    # テスト用ルームにはテストユーザーと管理者
    test_room = rooms[2]
    test_users = User.query.filter(User.username.like('member%')).all()  # memberで始まるユーザー
    admin = User.query.filter_by(username='admin').first()
    all_test_users = test_users + [admin]
    for user in all_test_users:
        role = 'owner' if user.username == 'admin' else 'member'
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
                role='owner'  # 匿名でもオーナーロール
            )
            db.session.add(anon_member)

        # 一般ユーザーを数人追加
        general_users = User.query.filter(User.username.in_(['member1', 'member2', 'member3'])).all()
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
    member1 = User.query.filter_by(username='member1').first()

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
            'user_id': member1.id,
            'display_name': member1.display_name,
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
                    'user_id': member1.id,
                    'display_name': member1.display_name,
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

    db.session.commit()
    return created_sessions

def create_master_data():
    """マスタテーブルに初期データを投入"""
    print("マスタデータ作成中...")

    # 1. ユーザーロールマスタの初期データ
    user_roles_data = [
        ('admin', '管理者', 'システム全体の管理権限', True, True, True, True, 1, True),
        ('sub_admin', '副管理者', 'ユーザー管理権限', False, True, True, True, 2, True),
        ('moderator', 'モデレーター', 'コンテンツ管理権限', False, False, True, True, 3, True),
        ('member', 'メンバー', '一般ユーザー権限', False, False, False, False, 4, True),
        ('guest', 'ゲスト', 'ゲスト権限（制限あり）', False, False, False, False, 5, True),
        ('developer', '開発者', '開発・デバッグ用権限', True, True, True, True, 6, True)
    ]

    for role_code, role_name, description, can_edit_master, can_edit_user, can_view_master, can_view_user, display_order, is_system in user_roles_data:
        db.session.execute(db.text("""
            INSERT INTO m_user_roles (role_code, role_name, description, can_edit_master, can_edit_user, can_view_master, can_view_user, display_order, is_system)
            VALUES (:role_code, :role_name, :description, :can_edit_master, :can_edit_user, :can_view_master, :can_view_user, :display_order, :is_system)
            ON CONFLICT (role_code) DO NOTHING
        """), {
            'role_code': role_code,
            'role_name': role_name,
            'description': description,
            'can_edit_master': can_edit_master,
            'can_edit_user': can_edit_user,
            'can_view_master': can_view_master,
            'can_view_user': can_view_user,
            'display_order': display_order,
            'is_system': is_system
        })

    # 2. ユーザーステータスマスタの初期データ
    user_statuses_data = [
        ('online', 'オンライン', 'アクティブ状態', 1, True),
        ('away', '離席中', '一時的に離席', 2, True),
        ('busy', '取り込み中', '忙しい状態', 3, True),
        ('offline', 'オフライン', '非アクティブ状態', 4, True),
        ('invisible', '隠れ身', 'オンラインだが非表示', 5, True)
    ]

    for status_code, status_name, description, display_order, is_system in user_statuses_data:
        db.session.execute(db.text("""
            INSERT INTO m_user_statuses (status_code, status_name, description, display_order, is_system)
            VALUES (:status_code, :status_name, :description, :display_order, :is_system)
            ON CONFLICT (status_code) DO NOTHING
        """), {
            'status_code': status_code,
            'status_name': status_name,
            'description': description,
            'display_order': display_order,
            'is_system': is_system
        })

    # 3. ルームタイプマスタの初期データ
    room_types_data = [
        ('group', 'グループチャット', '複数人でのチャット', 1, True),
        ('one_on_one', '1対1チャット', '2人だけのプライベートチャット', 2, True),
        ('support', 'サポート', 'サポート用チャット', 3, True),
        ('announcement', 'お知らせ', '管理者からのお知らせ専用', 4, True)
    ]

    for type_code, type_name, description, display_order, is_system in room_types_data:
        db.session.execute(db.text("""
            INSERT INTO m_room_types (type_code, type_name, description, display_order, is_system)
            VALUES (:type_code, :type_name, :description, :display_order, :is_system)
            ON CONFLICT (type_code) DO NOTHING
        """), {
            'type_code': type_code,
            'type_name': type_name,
            'description': description,
            'display_order': display_order,
            'is_system': is_system
        })

    # 4. メッセージタイプマスタの初期データ
    message_types_data = [
        ('text', 'テキスト', '通常のテキストメッセージ', 1, True),
        ('system', 'システム', 'システム自動生成メッセージ', 2, True),
        ('image', '画像', '画像ファイル', 3, True),
        ('file', 'ファイル', 'ファイル添付', 4, True),
        ('emoji', '絵文字', '絵文字リアクション', 5, True)
    ]

    for type_code, type_name, description, display_order, is_system in message_types_data:
        db.session.execute(db.text("""
            INSERT INTO m_message_types (type_code, type_name, description, display_order, is_system)
            VALUES (:type_code, :type_name, :description, :display_order, :is_system)
            ON CONFLICT (type_code) DO NOTHING
        """), {
            'type_code': type_code,
            'type_name': type_name,
            'description': description,
            'display_order': display_order,
            'is_system': is_system
        })

    # 5. ルーム内ロールマスタの初期データ
    room_roles_data = [
        ('owner', 'オーナー', 'ルーム作成者・全権限', True, True, True, True, 1, True),
        ('admin', '管理者', 'ルーム管理権限', True, True, True, True, 2, True),
        ('moderator', 'モデレーター', 'メッセージ管理権限', True, True, False, True, 3, True),
        ('member', 'メンバー', '一般参加者', False, False, False, False, 4, True),
        ('guest', 'ゲスト', 'ゲスト参加者（制限あり）', False, False, False, False, 5, True)
    ]

    for role_code, role_name, description, can_invite, can_kick, can_edit_room, can_delete_messages, display_order, is_system in room_roles_data:
        db.session.execute(db.text("""
            INSERT INTO m_room_roles (role_code, role_name, description, can_invite, can_kick, can_edit_room, can_delete_messages, display_order, is_system)
            VALUES (:role_code, :role_name, :description, :can_invite, :can_kick, :can_edit_room, :can_delete_messages, :display_order, :is_system)
            ON CONFLICT (role_code) DO NOTHING
        """), {
            'role_code': role_code,
            'role_name': role_name,
            'description': description,
            'can_invite': can_invite,
            'can_kick': can_kick,
            'can_edit_room': can_edit_room,
            'can_delete_messages': can_delete_messages,
            'display_order': display_order,
            'is_system': is_system
        })

    # 6. 言語マスタの初期データ
    languages_data = [
        ('ja', '日本語', 1, True),
        ('en', 'English', 2, True),
        ('zh', '中文', 3, True),
        ('ko', '한국어', 4, True)
    ]

    for lang_code, lang_name, display_order, is_system in languages_data:
        db.session.execute(db.text("""
            INSERT INTO m_languages (lang_code, lang_name, display_order, is_system)
            VALUES (:lang_code, :lang_name, :display_order, :is_system)
            ON CONFLICT (lang_code) DO NOTHING
        """), {
            'lang_code': lang_code,
            'lang_name': lang_name,
            'display_order': display_order,
            'is_system': is_system
        })

    db.session.commit()
    print("マスタデータ作成完了")

def main():
    """メイン処理"""
    app = create_app()

    with app.app_context():
        try:
            # 既存データを削除
            clear_existing_data()

            # マスタデータを作成
            create_master_data()

            # 初期ユーザーを作成
            create_initial_users()

            # 匿名ユーザーのセッションを作成
            create_anonymous_sessions()

            # 初期ルームを作成
            rooms = create_initial_rooms()

            # ルームメンバーを作成
            room_create_members(rooms)

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
