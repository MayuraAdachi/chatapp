# チャットルーム関連のコントローラー（関数形式）
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import validate_csrf, ValidationError
from app.services.room_service import RoomService
from app.models.room import get_room_owner
from app.forms.room_forms import RoomCreateForm, AnonymousUserForm, RoomJoinForm
import logging

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

def join_room():
    """
    ルームに参加（Ajax）
    """
    if request.method == 'POST':
        room_id = request.json.get('room_id')
        password = request.json.get('password', '')

        if not room_id:
            return jsonify({
                'success': False,
                'message': 'ルームIDが指定されていません'
            })

        try:
            result = RoomService.join_room(room_id, password)
            # redirectUrlがなければ部屋名を取得して生成
            if result.get('success'):
                redirectUrl = result.get('redirectUrl')
                if not redirectUrl:
                    # 部屋名取得
                    room_data = RoomService.get_room_for_chat(room_id)
                    if room_data.get('success'):
                        room_name = room_data['room']['name']
                        redirectUrl = f"/room/chat/{room_name}?room_id={room_id}"
                    else:
                        redirectUrl = f"/room/chat/?room_id={room_id}"
                result['redirectUrl'] = redirectUrl
            return jsonify(result)
        except Exception as e:
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

def room_create():
    """
    新しいルームを作成（WTForms使用）
    """
    form = RoomCreateForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # フォームが有効な場合の処理
            result = RoomService.room_create(
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
    if request.method == 'POST':
        try:
            result = RoomService.delete_room(room_id)

            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
        except Exception as e:
            flash(f'削除処理中にエラーが発生しました: {str(e)}', 'error')

    # リダイレクト先を明示的に指定
    return redirect('/room/')

def validate_room_create_form():
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

def chat(room_name):
    """
    チャット画面を表示（部屋名＋room_idクエリ指定）
    """
    try:
        from urllib.parse import unquote
        room_name = unquote(room_name)
        room_id = request.args.get('room_id')
        if not room_id:
            flash('部屋IDが指定されていません', 'error')
            return redirect(url_for('room.index'))
        room_data = RoomService.get_room_for_chat(room_id)
        if not room_data['success']:
            flash(room_data['message'], 'error')
            return redirect(url_for('room.index'))
        permissions = RoomService.get_user_permissions()
        return render_template(
            'room/chat.html',
            room=room_data['room'],
            username=permissions.get('username', 'ゲスト'),
            user_id=permissions.get('user_id'),
            is_owner=room_data.get('is_owner', False),
            is_admin=permissions.get('is_admin', False) or permissions.get('is_developer', False)
        )
    except Exception as e:
        flash(f'チャット画面の読み込み中にエラーが発生しました: {str(e)}', 'error')
        return redirect(url_for('room.index'))
