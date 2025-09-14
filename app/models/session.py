from app.extensions import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = 't_sessions'
    id = db.Column(db.String(255), primary_key=True)
    display_name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(64))  # INET型はSQLAlchemy標準ではstrでOK
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_active = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Session {self.id}>'
