from app.extensions import db
from sqlalchemy.dialects.postgresql import ENUM, UUID
from datetime import datetime
import uuid

member_role_enum = ENUM('creator', 'admin', 'member', name='member_role', create_type=False)

class RoomMember(db.Model):
    __tablename__ = 'room_members'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = db.Column(UUID(as_uuid=True), db.ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    session_id = db.Column(db.String(255))
    display_name = db.Column(db.String(100), nullable=False)
    role = db.Column(member_role_enum, default='member', nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_active = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.CheckConstraint('(user_id IS NOT NULL OR session_id IS NOT NULL)', name='check_member'),
        db.UniqueConstraint('room_id', 'user_id', name='unique_user_room'),
        db.UniqueConstraint('room_id', 'session_id', name='unique_session_room'),
    )

    def __repr__(self):
        return f'<RoomMember {self.id} room={self.room_id}>'
