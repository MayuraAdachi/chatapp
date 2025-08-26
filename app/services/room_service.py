# 部屋関連のビジネスロジック
from app.models.room import add_room as model_add_room, get_rooms as model_get_rooms, get_room_owner, delete_room as model_delete_room

# 部屋を追加
def add_room(room_name, owner_id=None):
    # ここでバリデーションや追加ロジックを実装
    if not room_name or len(room_name) > 100:
        return False
    return model_add_room(room_name, owner_id)

# 部屋一覧取得
def get_rooms():
    return model_get_rooms()

# 部屋オーナー取得
def get_room_owner(room_name):
    return get_room_owner(room_name)

# 部屋削除
def delete_room(room_name, owner_id=None):
    # ここで権限チェックや追加ロジックを実装
    return model_delete_room(room_name, owner_id)
