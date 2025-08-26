# routes/room_routes.py
# チャットルーム関連のルーティング（URLとコントローラーの対応）をまとめたファイル。
# Blueprintでルート定義し、コントローラー関数を呼び出す。

from flask import Blueprint
from app.controllers import room_controller

room_bp = Blueprint('room', __name__)

# ユーザー識別用のセッションIDをセット
room_bp.before_app_request(room_controller.set_user)

room_bp.route('/', methods=['GET', 'POST'])(room_controller.index)
# # room_bp.route('/rooms', methods=['GET', 'POST'])(room_controller.login)
# room_bp.route('/delete_room/<room_name>', methods=['POST'])(room_controller.delete_room_route)
# room_bp.route('/room/<room_name>')(room_controller.room)
