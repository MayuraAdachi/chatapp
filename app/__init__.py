# app/__init__.py
# 初期化や設定を行う
import os
from flask import Flask, request, session
from dotenv import load_dotenv
from app.config import const
from .extensions import db, socketio, babel, csrf
# 新しいルーティング構成を使用
from app.routes import register_blueprints

def configure_app_settings(app):
    """アプリケーションの基本設定を行う"""
    # Flaskの基本設定
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ファイルアップロードの設定（10MB）
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

    # CSRF保護の設定
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = int(const.CSRF_TOKEN_EXPIRY)

    # アプリ名・バージョン・デバッグモードの設定
    app.config['APP_TITLE'] = const.APP_TITLE
    app.config['VERSION'] = const.VERSION
    debug_mode = os.getenv('DEBUG_MODE', 'False').lower() in ['true', '1', 'yes']
    app.config['DEBUG_MODE'] = debug_mode
    app.debug = debug_mode

    # 開発モードの場合はキャッシュを無効化
    if app.debug:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # チャットログの保存日数（通常・バックアップ）の設定
    app.config['CHAT_LOG_DAYS'] = int(const.CHAT_LOG_DAYS)
    app.config['CHAT_BACKUP_DAYS'] = int(const.CHAT_BACKUP_DAYS)

def initialize_extensions(app):
    """拡張機能の初期化を行う"""
    db.init_app(app)
    csrf.init_app(app)

    # CSRF保護の除外設定（一時的に無効化）
    # @csrf.exempt
    # def csrf_exempt_for_room_join():
    #     # ルーム参加APIをCSRF保護から除外
    #     return request.endpoint == 'room.join_room'

    socketio.init_app(app)  # async_modeはextensions.pyで指定

    if babel:
        babel.init_app(app)

def configure_babel_locale(app):
    """Babelのロケール設定を行う"""
    if not babel:
        return None

    # 言語設定
    app.config['LANGUAGES'] = const.SUPPORTED_LANGUAGES
    app.config['BABEL_DEFAULT_LOCALE'] = const.DEFAULT_LANGUAGE
    app.config['BABEL_DEFAULT_TIMEZONE'] = const.DEFAULT_TIMEZONE

    # ロケールセレクター（バージョン互換性を考慮）
    def get_locale():
        # 1. URL パラメータから言語を取得
        if request.args.get('lang'):
            lang = request.args.get('lang')
            if lang in app.config['LANGUAGES']:
                session['language'] = lang
                if app.debug:  # デバッグモードの場合のみ出力
                    print(f"Locale: {lang} (from URL)")
                return lang

        # 2. セッションから言語を取得
        if 'language' in session and session['language'] in app.config['LANGUAGES']:
            if app.debug:  # デバッグモードの場合のみ出力
                print(f"Locale: {session['language']} (from session)")
            return session['language']

        # 3. ブラウザの優先言語を使用
        browser_lang = request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'ja'
        if app.debug:  # デバッグモードの場合のみ出力
            print(f"Locale: {browser_lang} (from browser)")
        return browser_lang

    # Flask-Babelのバージョンに応じてロケールセレクターを設定
    try:
        # Flask-Babel 2.0+ の新しい方法
        babel.locale_selector_func = get_locale
        if app.debug:
            print("Locale selector set using babel.locale_selector_func")
    except AttributeError:
        try:
            # Flask-Babel 1.0 の方法
            babel.locale_selector(get_locale)
            if app.debug:
                print("Locale selector set using babel.locale_selector")
        except AttributeError:
            try:
                # さらに古いバージョン
                babel.localeselector(get_locale)
                if app.debug:
                    print("Locale selector set using babel.localeselector")
            except AttributeError:
                print("Warning: Could not set locale selector")

    return get_locale

def configure_fallback_translation(app):
    """Babelが利用できない場合の翻訳機能設定"""
    def simple_gettext(text):
        return text

    app.jinja_env.globals.update(_=simple_gettext, _n=lambda s, p, n: s if n == 1 else p)

def configure_translation_functions(app, get_locale_func):
    """翻訳関数の設定を行う"""
    if not babel:
        # Babelが利用できない場合はフォールバック
        configure_fallback_translation(app)
        return

    # テンプレートで翻訳機能を使用できるようにする
    try:
        from flask_babel import gettext, ngettext

        def enhanced_gettext(text):
            """Babel翻訳関数（自動翻訳フォールバック付き）"""
            try:
                # 現在の言語を取得
                current_lang = get_locale_func() if get_locale_func else 'ja'

                # 日本語の場合は翻訳せずにそのまま返す
                if current_lang == 'ja':
                    return text

                # デバッグ情報を出力（開発モード時）
                if app.debug:
                    print(f"Translation Debug: '{text}' -> lang={current_lang}")

                # Babel翻訳を試す
                translated = gettext(text)
                if app.debug:
                    print(f"Babel result: '{text}' -> '{translated}'")

                if translated != text:  # 翻訳が見つかった場合
                    return translated

                # Babel翻訳がない場合、日本語以外なら自動翻訳を試す
                if current_lang != 'ja':
                    try:
                        from app.utils.auto_translator import translate_auto
                        auto_translated = translate_auto(text, current_lang)
                        if auto_translated != text:
                            if app.debug:
                                print(f"Auto translation: '{text}' -> '{auto_translated}'")
                            return auto_translated
                    except Exception as auto_error:
                        if app.debug:
                            print(f"Auto translation error: {auto_error}")

                return text

            except Exception as e:
                if app.debug:
                    print(f"Translation error: {e}")
                return text

        app.jinja_env.globals.update(_=enhanced_gettext, _n=ngettext)
    except ImportError:
        # Flask-Babelがない場合はフォールバック
        configure_fallback_translation(app)

def register_app_blueprints(app):
    """Blueprintの登録を行う（役割別分割）"""
    # 新しい役割別分割ルーティングを使用
    from app.routes import register_blueprints
    register_blueprints(app)

def register_context_processors(app):
    """コンテキストプロセッサーを登録"""
    from app.utils.context_processors import user_context
    app.context_processor(user_context)

# Flaskのセットアップ
def create_app():
    """Flaskアプリケーションを作成・設定する"""
    # .envファイルから環境変数を読み込む
    load_dotenv()

    # Flaskアプリケーションのインスタンスを作成
    app = Flask(__name__)

    # 各種設定を行う
    configure_app_settings(app)
    initialize_extensions(app)

    # Babel設定（ロケール関数を取得）
    get_locale_func = configure_babel_locale(app)

    # 翻訳機能の設定
    configure_translation_functions(app, get_locale_func)

    # Blueprintの登録
    register_app_blueprints(app)
    register_context_processors(app)

    return app
