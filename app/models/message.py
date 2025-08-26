# メッセージ（チャットログ）管理モデル
from app.extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime
from flask import current_app

message_type_enum = ENUM('text', 'system', name='message_type', create_type=False)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    session_id = db.Column(db.String(255))
    display_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(message_type_enum, default='text', nullable=False)
    reply_to = db.Column(db.Integer, db.ForeignKey('messages.id'))
    edited = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_room = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Message {self.id} room={self.room_id} user={self.user_id}>'

# メッセージ追加
def add_message(user_id, room_id, content, message_type='text', session_id=None, display_name=None, reply_to=None):
    msg = Message(
        user_id=user_id,
        room_id=room_id,
        content=content,
        message_type=message_type,
        session_id=session_id,
        display_name=display_name,
        reply_to=reply_to
    )
    db.session.add(msg)
    db.session.commit()
    return msg

# 3日分のメッセージ取得
def get_recent_messages(room_id):
    from datetime import datetime, timedelta
    days = current_app.config.get('CHAT_LOG_DAYS', 3)
    limit_date = datetime.utcnow() - timedelta(days=days)
    return Message.query.filter_by(room_id=room_id, deleted_room=False).filter(Message.created_at >= limit_date).order_by(Message.created_at.asc()).all()

# バックアップ用（削除済み部屋の1週間分）
def get_backup_messages(room_id):
    from datetime import datetime, timedelta
    days = current_app.config.get('CHAT_BACKUP_DAYS', 7)
    limit_date = datetime.utcnow() - timedelta(days=days)
    return Message.query.filter_by(room_id=room_id, deleted_room=True).filter(Message.created_at >= limit_date).order_by(Message.created_at.asc()).all()

# 部屋削除時に論理削除フラグを立てる
def mark_room_deleted(room_id):
    Message.query.filter_by(room_id=room_id).update({'deleted_room': True})
    db.session.commit()

# 1週間以上前のバックアップを物理削除
def delete_old_backups():
    from datetime import datetime, timedelta
    days = current_app.config.get('CHAT_BACKUP_DAYS', 7)
    limit_date = datetime.utcnow() - timedelta(days=days)
    Message.query.filter(Message.deleted_room == True, Message.created_at < limit_date).delete()
    db.session.commit()
