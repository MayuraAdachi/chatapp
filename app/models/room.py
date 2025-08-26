# app/models/room.py
# チャットルーム（SQLAlchemyモデル版）

from app.extensions import db
from sqlalchemy.dialects.postgresql import ENUM, UUID
from datetime import datetime, timezone
import uuid

room_type_enum = ENUM('group', 'one_on_one', name='room_type', create_type=False)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(room_type_enum, default='group', nullable=False)
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    password_hash = db.Column(db.String(255))
    max_members = db.Column(db.Integer, default=50, nullable=False)
    created_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    created_by_session = db.Column(db.String(255))
    created_by_name = db.Column(db.String(100))
    message_retention_days = db.Column(db.Integer, default=30, nullable=False)
    max_message_count = db.Column(db.Integer, default=300, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f'<Room {self.name}>'

def add_room(room_name, owner_id=None, session_id=None, creator_name=None, description=None, max_members=50, has_password=False, room_password=None):
    # 既存のルーム名チェック
    if Room.query.filter_by(name=room_name).first():
        return False  # 既に存在する場合はFalseを返す

    # パスワードハッシュ化
    password_hash = None
    if has_password and room_password:
        from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash(room_password)

    room = Room(
        name=room_name,
        description=description,
        max_members=max_members,
        is_private=has_password,  # パスワード有りの場合はプライベート扱い
        password_hash=password_hash,
        created_by_user_id=owner_id,
        created_by_session=session_id,
        created_by_name=creator_name
    )
    db.session.add(room)
    db.session.commit()
    return True  # 成功時はTrueを返す

def get_rooms():
    """すべてのルーム情報を取得"""
    return Room.query.all()

def get_room_by_id(room_id):
    """IDでルームを取得"""
    return Room.query.get(room_id)

def get_room_by_name(room_name):
    """名前でルームを取得"""
    return Room.query.filter_by(name=room_name).first()

def get_room_owner_name(room):
    """ルームオーナーのユーザー名を取得"""
    from app.models.user import User

    # created_by_nameが存在する場合は優先して使用
    if hasattr(room, 'created_by_name') and room.created_by_name:
        return room.created_by_name

    # 登録ユーザーでcreated_by_nameが無い場合のフォールバック
    if hasattr(room, 'created_by_user_id') and room.created_by_user_id:
        user = User.query.get(room.created_by_user_id)
        if user:
            return user.username
        else:
            return 'Unknown User'
    elif hasattr(room, 'created_by_session') and room.created_by_session:
        # セッション情報のみの匿名ユーザーの場合
        return '匿名ユーザー'
    else:
        # 旧形式（文字列）の場合の処理
        room_obj = Room.query.filter_by(name=room).first()
        if room_obj:
            if room_obj.created_by_user_id:
                user = User.query.get(room_obj.created_by_user_id)
                return user.username if user else 'Unknown User'
            elif room_obj.created_by_name:
                return room_obj.created_by_name
            else:
                return '匿名ユーザー'
        return 'Unknown User'


# 後方互換性のために旧関数名も残す
def get_room_owner(room):
    """ルームオーナーのユーザー名を取得（後方互換性のため）"""
    return get_room_owner_name(room)

def delete_room_by_id(room_id):
    """IDでルームを削除"""
    room = Room.query.get(room_id)
    if room:
        db.session.delete(room)
        db.session.commit()
        return True
    return False

def delete_room(room_name, owner_id=None):
    room = Room.query.filter_by(name=room_name).first()
    if room:
        if owner_id is None or room.created_by_user_id == owner_id:
            db.session.delete(room)
            db.session.commit()
            return True
    return False

def get_room_id(room_name):
    room = Room.query.filter_by(name=room_name).first()
    return room.id if room else None
