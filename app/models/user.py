# ユーザー情報の管理（SQLAlchemyモデル版）

from app.extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

user_role_enum = ENUM('developer', 'admin', 'member', name='user_role', create_type=False)
user_status_enum = ENUM('online', 'offline', 'away', name='user_status', create_type=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    role = db.Column(user_role_enum, default='member', nullable=False)
    avatar_url = db.Column(db.String(255))
    status = db.Column(user_status_enum, default='offline', nullable=False)
    last_seen = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

def regist_user(username, password, email=None):
    from sqlalchemy import text
    # パスワードはpgcryptoのcryptでハッシュ化
    sql = text("""
        INSERT INTO users (username, email, password_hash, display_name, role)
        VALUES (:username, :email, crypt(:password, gen_salt('bf')), :display_name, :role)
        RETURNING id
    """)
    # email, display_name, roleは適宜引数やデフォルト値で補完
    if not email:
        email = f'{username}@example.com'
    params = dict(username=username, email=email, password=password, display_name=username, role='member')
    result = db.session.execute(sql, params)
    db.session.commit()
    return result.fetchone() is not None

def authenticate_user(username, password):
    from sqlalchemy import text
    sql = text("""
        SELECT * FROM users WHERE username=:username AND password_hash=crypt(:password, password_hash)
    """)
    result = db.session.execute(sql, {'username': username, 'password': password})
    return result.fetchone() is not None
