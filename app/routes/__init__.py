# -----------------------------------
# ルーティングパッケージの初期化用ファイル
# -----------------------------------
from .room_routes import room_bp
from .auth_routes import auth_bp

__all__ = ['room_bp', 'auth_bp']
