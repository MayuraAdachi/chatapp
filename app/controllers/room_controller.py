# チャットルーム関連のコントローラー（関数形式）
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import validate_csrf, ValidationError
from app.services.room_service import RoomService
from app.models.room import get_room_owner
from app.forms.room_forms import RoomCreateForm, AnonymousUserForm, RoomJoinForm

def is_authenticated():
    """
    ログイン状態をチェック（登録ユーザーかどうか）
    """
    return RoomService.is_authenticated()

def set_user():
    """
    セッションにユーザーIDがなければ新規生成
    """
    RoomService.set_user_session()

def chat(room_id):
    """
    チャット画面を表示
    """
    try:
        # ルーム情報を取得
        room_data = RoomService.get_room_for_chat(room_id)

        if not room_data['success']:
            flash(room_data['message'], 'error')
            return redirect(url_for('room.index'))

        # ユーザー権限を取得
        permissions = RoomService.get_user_permissions()

        return render_template('room/chat.html',
                                room=room_data['room'],
                                username=permissions['username'] or 'ゲスト',
                                user_id=permissions['user_id'],
                                is_owner=room_data['is_owner'],
                                is_admin=permissions['is_admin'] or permissions['is_developer'])

    except Exception as e:
        flash(f'チャット画面の読み込み中にエラーが発生しました: {str(e)}', 'error')
        return redirect(url_for('room.index'))

def join_room():
    """
    ルームに参加（Ajax）
    """
    print(f"join_room called: method={request.method}, content_type={request.content_type}")
    print(f"request.headers: {dict(request.headers)}")
    print(f"request.json: {request.json}")

    if request.method == 'POST':
        # 一時的にCSRF検証をスキップ（開発用）
        # CSRFトークンの検証
        # try:
        #     csrf_token = request.headers.get('X-CSRFToken')
        #     if csrf_token:
        #         validate_csrf(csrf_token)
        #         print("CSRF token validation successful")
        # except ValidationError as e:
        #     print(f"CSRF token validation failed: {e}")
        #     return jsonify({
        #         'success': False,
        #         'message': 'CSRF token validation failed'
        #     }), 400

        room_id = request.json.get('room_id')
        password = request.json.get('password', '')

        print(f"room_id: {room_id}, password: {password}")

        if not room_id:
            return jsonify({
                'success': False,
                'message': 'ルームIDが指定されていません'
            })

        try:
            result = RoomService.join_room(room_id, password)
            print(f"join result: {result}")
            return jsonify(result)
        except Exception as e:
            print(f"join error: {e}")
            return jsonify({
                'success': False,
                'message': f'参加処理中にエラーが発生しました: {str(e)}'
            })

    return jsonify({
        'success': False,
        'message': '不正なリクエストです'
    })

def index():
    """
    ルーム一覧の表示・匿名参加の処理
    """
    # フォームのインスタンスを作成
    anonymous_form = AnonymousUserForm()
    create_form = RoomCreateForm()

    # セッションの整合性をチェック・クリーンアップ
    RoomService.validate_and_cleanup_session()

    if request.method == 'POST':
        # 匿名参加の処理（トップページから）
        if 'username' in request.form and anonymous_form.validate_on_submit():
            username = anonymous_form.username.data
            if RoomService.handle_anonymous_user_registration(username):
                # ルーム一覧を表示
                data = RoomService.get_all_rooms_with_permissions()
                return render_template('room/index.html',
                                        rooms=data['rooms'],
                                        get_room_owner=get_room_owner,
                                        user_id=data['permissions']['user_id'],
                                        user_role=data['permissions']['user_role'],
                                        anonymous_form=anonymous_form,
                                        create_form=create_form)

        # 既存ユーザーの名前変更（匿名ユーザーのみ）
        if 'set_name' in request.form and anonymous_form.validate_on_submit():
            username = anonymous_form.username.data
            if RoomService.update_anonymous_username(username):
                return redirect(url_for('room.index'))

        # ルーム作成（簡易版）
        if 'room_name' in request.form and not 'username' in request.form:
            room_name = request.form.get('room_name')
            if RoomService.handle_room_creation_from_index(room_name):
                return redirect(url_for('room.index'))
            else:
                flash('ルームの作成に失敗しました', 'error')

    # GET リクエストまたは処理完了後
    data = RoomService.get_all_rooms_with_permissions()
    return render_template('room/index.html',
                            rooms=data['rooms'],
                            get_room_owner=get_room_owner,
                            user_id=data['permissions']['user_id'],
                            user_role=data['permissions']['user_role'],
                            anonymous_form=anonymous_form,
                            create_form=create_form)

def create_room():
    """
    新しいルームを作成（WTForms使用）
    """
    form = RoomCreateForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # フォームが有効な場合の処理
            result = RoomService.create_room(
                room_name=form.room_name.data,
                description=form.room_description.data,
                max_members=form.max_members.data,
                room_password=form.room_password.data if form.room_password.data else None
            )

            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
        else:
            # フォームバリデーションエラーの場合
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{form[field].label.text}: {error}', 'error')

    return redirect(url_for('room.index'))

def delete_room(room_id):
    """
    ルームを削除（管理者、開発者、作成者のみ）
    """
    print(f"delete_room called: method={request.method}, room_id={room_id}")

    if request.method == 'POST':
        try:
            result = RoomService.delete_room(room_id)
            print(f"delete result: {result}")

            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
        except Exception as e:
            print(f"delete error: {e}")
            flash(f'削除処理中にエラーが発生しました: {str(e)}', 'error')

    # リダイレクト先を明示的に指定
    return redirect('/room/')

def validate_room_form():
    """
    Ajax用のルーム作成フォームバリデーション
    """
    form = RoomCreateForm()

    if form.validate_on_submit():
        return jsonify({
            'success': True,
            'message': 'バリデーション成功'
        })
    else:
        errors = {}
        for field, error_messages in form.errors.items():
            errors[field] = error_messages

        return jsonify({
            'success': False,
            'errors': errors
        })

def chat_by_name(room_name):
    """
    チャット画面を表示（部屋名指定）
    """
    try:
        # URLデコードを行う
        from urllib.parse import unquote
        room_name = unquote(room_name)

        # ルーム情報を取得（部屋名から）
        room_data = RoomService.get_room_for_chat_by_name(room_name)

        if not room_data['success']:
            flash(room_data['message'], 'error')
            return redirect(url_for('room.index'))

        # ユーザー権限を取得
        permissions = RoomService.get_user_permissions()

        return render_template('room/chat.html',
                                room=room_data['room'],
                                username=permissions['username'] or 'ゲスト',
                                user_id=permissions['user_id'],
                                is_owner=room_data['is_owner'],
                                is_admin=permissions['is_admin'] or permissions['is_developer'])

    except Exception as e:
        flash(f'チャット画面の読み込み中にエラーが発生しました: {str(e)}', 'error')
        return redirect(url_for('room.index'))
