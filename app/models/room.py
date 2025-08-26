# app/models/room.py
# チャットルームのデータ管理（SQLAlchemyモデル版）

from app.extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

room_type_enum = ENUM('group', 'one_on_one', name='room_type', create_type=False)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(room_type_enum, default='group', nullable=False)
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    password_hash = db.Column(db.String(255))
    max_members = db.Column(db.Integer, default=50, nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by_session = db.Column(db.String(255))
    message_retention_days = db.Column(db.Integer, default=30, nullable=False)
    max_message_count = db.Column(db.Integer, default=300, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Room {self.name}>'

def add_room(room_name, owner_id=None):
    if Room.query.filter_by(name=room_name).first():
        return
    room = Room(name=room_name, owner_id=owner_id)
    db.session.add(room)
    db.session.commit()

def get_rooms():
    return [room.name for room in Room.query.all()]

def get_room_owner(room_name):
    room = Room.query.filter_by(name=room_name).first()
    return room.owner_id if room else None

def delete_room(room_name, owner_id=None):
    room = Room.query.filter_by(name=room_name).first()
    if room:
        if owner_id is None or room.owner_id == owner_id:
            db.session.delete(room)
            db.session.commit()
            return True
    return False

def get_room_id(room_name):
    room = Room.query.filter_by(name=room_name).first()
    return room.id if room else None
