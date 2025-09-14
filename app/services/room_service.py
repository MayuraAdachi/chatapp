# app/services/room_service.py
"""
ルーム関連のビジネスロジックを提供するサービス層
"""
from flask import session, flash
from app.models.room import (
    add_room as model_add_room,
    get_rooms as model_get_rooms,
    get_room_by_id,
    delete_room_by_id,
)
from app.models.message import mark_room_deleted
import uuid


class RoomService:
    """ルーム関連サービス"""

    @staticmethod
    def is_authenticated():
        """
        ログイン状態をチェック（登録ユーザーかどうか）
        :return: 登録ユーザーでログイン中かどうか
        """
        return session.get('is_logged_in', False) and 'user_id' in session

    @staticmethod
    def set_user_session():
        """
        セッションにユーザーIDがなければ新規生成
        """
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())

    @staticmethod
    def get_user_permissions():
        """
        現在のユーザーの権限情報を取得
        :return: dict - 権限情報
        """
        user_role = session.get('role', 'member')
        return {
            'is_admin': user_role == 'admin',
            'is_developer': user_role == 'developer',
            'user_role': user_role,
            'user_id': session.get('user_id'),
            'username': session.get('username'),
            'is_logged_in': RoomService.is_authenticated()
        }

    @staticmethod
    def get_all_rooms_with_permissions():
        """
        すべてのルームを権限情報と共に取得
        :return: dict - ルーム情報と権限情報
        """
        rooms = model_get_rooms()
        permissions = RoomService.get_user_permissions()

        return {
            'rooms': rooms,
            'permissions': permissions
        }

    @staticmethod
    def handle_anonymous_user_registration(username):
        """
        匿名ユーザーの登録処理
        :param username: ユーザー名
        :return: bool - 成功かどうか
        """
        if not username:
            return False

        if not session.get('username') and not RoomService.is_authenticated():
            session['username'] = username
            flash(f'ようこそ、{username}さん！', 'success')
            return True

        return False

    @staticmethod
    def update_anonymous_username(username):
        """
        匿名ユーザーの名前変更
        :param username: 新しいユーザー名
        :return: bool - 成功かどうか
        """
        if not username or RoomService.is_authenticated():
            return False

        session['username'] = username
        flash('名前を設定しました', 'success')
        return True

    @staticmethod
    def room_create(room_name, description=None, max_members=50, room_password=None):
        """
        新しいルームを作成
        :param room_name: ルーム名
        :param description: ルーム説明
        :param max_members: 最大メンバー数
        :param room_password: ルームパスワード（空の場合は公開ルーム）
        :return: dict - 結果情報
        """
        result = {
            'success': False,
            'message': '',
            'room_name': room_name
        }

        user_id = session.get('user_id')

        # バリデーション
        if not room_name:
            result['message'] = 'ルーム名を入力してください'
            return result

        if not RoomService.is_authenticated():
            result['message'] = 'ルームを作成するにはログインが必要です'
            return result

        # 最大メンバー数の型変換のみ（範囲チェックはフォームで担保）
        if max_members is None:
            max_members = 50
        try:
            max_members = int(max_members)
        except (ValueError, TypeError):
            result['message'] = '最大メンバー数は数値で入力してください'
            return result
        has_password = bool(room_password and room_password.strip())

        if has_password:
            room_password = room_password.strip()
        else:
            room_password = None

        try:
            # ルーム作成実行（登録ユーザーのみ）
            creator_name = session.get('username')

            success = model_add_room(
                room_name,
                owner_id=user_id,
                creator_name=creator_name,
                description=description,
                max_members=max_members,
                has_password=has_password,
                room_password=room_password
            )

            if success is False:
                result['message'] = 'ルーム名が既に使用されています'
                return result

            result['success'] = True
            result['message'] = f'ルーム「{room_name}」を作成しました'

        except Exception as e:
            result['message'] = f'ルームの作成に失敗しました: {str(e)}'

        return result

    @staticmethod
    def delete_room(room_id):
        """
        ルームを削除（管理者、開発者、作成者のみ）
        :param room_id: ルームID
        :return: dict - 結果情報
        """
        result = {
            'success': False,
            'message': '',
            'room_id': room_id
        }

        user_id = session.get('user_id')

        # バリデーション
        if not user_id:
            result['message'] = 'ユーザーIDが見つかりません'
            return result

        try:
            # ルーム存在チェック
            room = get_room_by_id(room_id)
            if not room:
                result['message'] = 'ルームが見つかりません'
                return result

            # 権限チェック
            permissions = RoomService.get_user_permissions()
            is_admin = permissions['is_admin']
            is_developer = permissions['is_developer']

            # 作成者チェック（登録ユーザーのみ）
            is_owner = False
            if RoomService.is_authenticated() and room.created_by_user_id:
                # 登録ユーザーが作成したルーム
                is_owner = (str(room.created_by_user_id) == str(user_id))

            # 管理者・開発者は全てのルームを削除可能
            # 登録ユーザーは自分のルームを削除可能（匿名ユーザーはルーム作成不可のため削除権限なし）
            if not (is_admin or is_developer or is_owner):
                result['message'] = 'ルームを削除する権限がありません'
                return result

            # ルーム削除実行
            delete_room_by_id(room_id)

            # 関連メッセージも削除フラグを設定
            mark_room_deleted(room_id)

            result['success'] = True
            result['message'] = f'ルーム「{room.name}」を削除しました'

        except Exception as e:
            result['message'] = f'ルームの削除に失敗しました: {str(e)}'

        return result

    @staticmethod
    def handle_room_creation_from_index(room_name):
        """
        インデックスページからのルーム作成処理
        :param room_name: ルーム名
        :return: bool - 成功かどうか
        """
        if not room_name:
            return False

        user_id = session.get('user_id')
        try:
            model_add_room(room_name, owner_id=user_id)
            flash('ルームを作成しました', 'success')
            return True
        except Exception as e:
            flash(f'ルームの作成に失敗しました: {str(e)}', 'error')
            return False

    @staticmethod
    def join_room(room_id, password=''):
        """
        ルームに参加
        :param room_id: ルームID
        :param password: パスワード（必要な場合）
        :return: dict - 結果情報
        """
        result = {
            'success': False,
            'message': '',
            'redirectUrl': ''
        }

        user_id = session.get('user_id')

        if not user_id:
            result['message'] = 'ユーザー認証が必要です'
            return result

        try:
            # ルーム存在チェック
            room = get_room_by_id(room_id)

            if not room:
                result['message'] = 'ルームが見つかりません'
                return result

            # パスワードチェック（必要な場合）
            if hasattr(room, 'has_password') and room.has_password:
                if not password:
                    result['message'] = 'パスワードが必要です'
                    return result
                if hasattr(room, 'room_password') and room.room_password != password:
                    result['message'] = 'パスワードが正しくありません'
                    return result

            # 参加成功
            from urllib.parse import quote
            result['success'] = True
            result['message'] = f'ルーム「{room.name}」に参加しました'
            result['redirectUrl'] = f'/room/chat/{quote(room.name)}?room_id={room.id}'
            result['room_name'] = room.name

        except Exception as e:
            result['message'] = f'参加処理中にエラーが発生しました: {str(e)}'

        return result

    @staticmethod
    def validate_anonymous_session():
        """
        匿名セッションの妥当性を検証し、必要に応じてクリーンアップ
        :return: bool - セッションが有効かどうか
        """
        username = session.get('username')
        is_logged_in = session.get('is_logged_in', False)
        user_id = session.get('user_id')

        # ログインユーザーの場合は常に有効
        if is_logged_in and user_id:
            return True

        # 匿名ユーザーの場合
        if not is_logged_in and username and user_id:
            return True

        # 不整合な状態（ユーザー名はあるがuser_idがない等）をクリーンアップ
        if username and not user_id:
            session.pop('username', None)
            return False

        return True

    @staticmethod
    def validate_and_cleanup_session():
        """
        セッションの整合性をチェックし、不整合な状態をクリーンアップ
        タブを閉じて再アクセスした際のセッション状態を正常化
        """
        is_logged_in = session.get('is_logged_in', False)
        username = session.get('username')
        user_id = session.get('user_id')

        # ログインしていないのにユーザー名だけある場合のチェック
        if not is_logged_in and username:
            # 匿名ユーザーとしてのセッションが残っている場合
            if user_id:
                # user_idがあれば匿名ユーザーとして継続
                pass
            else:
                # user_idがない場合は不整合なセッション状態をクリア
                session.pop('username', None)

        # user_idがない場合は新規生成（匿名ユーザー用）
        if not user_id:
            session['user_id'] = str(uuid.uuid4())

    @staticmethod
    def get_room_for_chat(room_id):
        """
        チャット用のルーム情報をIDで取得
        :param room_id: ルームID
        :return: dict - ルーム情報と権限
        """
        room = get_room_by_id(room_id)
        if not room:
            return {
                'success': False,
                'message': '指定されたIDのルームが見つかりません',
                'room': None,
                'is_owner': False
            }
        permissions = RoomService.get_user_permissions()
        is_owner = False
        if hasattr(room, 'created_by_user_id') and permissions['user_id']:
            is_owner = (str(room.created_by_user_id) == str(permissions['user_id']))
        return {
            'success': True,
            'room': room,
            'is_owner': is_owner
        }
