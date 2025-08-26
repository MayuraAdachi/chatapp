# 役割別分割ルーティングの統合管理

def register_blueprints(app):
    """
    役割別に分割されたBlueprintを登録

    構成:
    - public.py: 一般ユーザー向け機能（main, room）
    - auth.py: 認証・ユーザー管理機能
    - admin.py: 管理者・開発者専用機能
    """

    # 公開機能のBlueprint登録
    try:
        from app.routes.public import public_blueprints
        for bp in public_blueprints:
            app.register_blueprint(bp)
    except ImportError as e:
        print(f"公開機能のインポートエラー: {e}")

    # 認証機能のBlueprint登録
    try:
        from app.routes.auth import auth_blueprints
        for bp in auth_blueprints:
            app.register_blueprint(bp)
    except ImportError as e:
        print(f"認証機能のインポートエラー: {e}")

    # 管理機能のBlueprint登録
    try:
        from app.routes.admin import admin_blueprints
        for bp in admin_blueprints:
            app.register_blueprint(bp)
    except ImportError as e:
        print(f"管理機能のインポートエラー: {e}")

# 新構成のエクスポート
__all__ = ['register_blueprints']
