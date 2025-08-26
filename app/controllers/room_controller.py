# チャットルーム関連のコントローラー（関数形式）
from flask import render_template, request, redirect, url_for, session, flash
from app.models.room import add_room, get_rooms, get_room_owner, delete_room
from app.models.message import mark_room_deleted
# room_id取得用関数をimport
from app.models.room import get_room_id
import uuid

def set_user():
    """
    セッションにユーザーIDがなければ新規生成
    """
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

def index():
    """
    トップページの表示
    """
    user_id = session.get('user_id')
    username = session.get('username')
    if request.method == 'POST':
        if 'set_name' in request.form:
            username = request.form.get('username')
            if username:
                session['username'] = username
                flash('名前を設定しました')
            return redirect(url_for('room.index'))
        room_name = request.form.get('room_name')
        add_room(room_name, owner_id=user_id)
        return redirect(url_for('room.index'))
    rooms = get_rooms()
    return render_template('index.html', rooms=rooms, user_id=user_id, get_room_owner=get_room_owner, username=username)

# def welcome():
#     if request.method == 'POST' and 'set_name' in request.form:
#         username = request.form.get('username')
#         if username:
#             session['username'] = username
#             flash('名前を設定しました')
#             return redirect(url_for('room.index'))
#     return render_template('welcome.html')

# def delete_room_route(room_name):
#     user_id = session['user_id']
#     # room_id取得
#     room_id = get_room_id(room_name)
#     if room_id is not None:
#         # メッセージ論理削除
#         mark_room_deleted(room_id)
#     if delete_room(room_name, owner_id=user_id):
#         return redirect(url_for('room.index'))
#     return '削除権限がありません', 403

# def room(room_name):
#     rooms = get_rooms()
#     if room_name not in rooms:
#         return redirect(url_for('room.index'))
#     return render_template('room.html', room_name=room_name)
