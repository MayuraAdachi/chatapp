# ユーザー情報の管理（SQLAlchemyモデル版）

from app.extensions import db
from sqlalchemy.dialects.postgresql import ENUM, UUID
from datetime import datetime
from werkzeug.security import check_password_hash
import uuid

user_role_enum = ENUM('developer', 'admin', 'member', name='user_role', create_type=False)
user_status_enum = ENUM('online', 'offline', 'away', 'busy', 'invisible', name='user_status', create_type=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    role = db.Column(user_role_enum, default='member', nullable=False)
    avatar_url = db.Column(db.String(255))
    profile_image = db.Column(db.String(255))  # プロフィール画像ファイル名
    bio = db.Column(db.Text)  # 自己紹介
    status = db.Column(user_status_enum, default='offline', nullable=False)
    status_message = db.Column(db.String(100))  # ステータスメッセージ
    last_seen = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def check_password(self, password):
        """パスワード検証（Werkzeugを使用）"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
