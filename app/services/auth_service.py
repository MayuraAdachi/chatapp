# ユーザー認証・登録関連のビジネスロジック
from flask import session, flash
from app.models.user import User
from app.forms.regist_form import RegistForm
from app.forms.login_form import LoginForm
from app.forms.password_change_form import PasswordChangeForm
from app.forms.profile_update_form import ProfileUpdateForm
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


def regist_validation(request):
    """
    アカウント登録の入力値バリデーション
    :param request: Flaskのリクエストオブジェクト
    :return: (フラグ, フォーム, エラー)
    """
    form = RegistForm(request.form)
    errors = {}
    if request.method == 'POST':
        if form.validate():
            return True, form, errors
        else:
            for field, field_errors in form.errors.items():
                errors[field] = field_errors[0]  # 最初のエラーのみ表示
    return False, form, errors


def login_validation(request):
    """
    ログインの入力値バリデーション
    :param request: Flaskのリクエストオブジェクト
    :return: (フラグ, フォーム, エラー)
    """
    form = LoginForm(request.form)
    errors = {}
    if request.method == 'POST':
        if form.validate():
            return True, form, errors
        else:
            for field, field_errors in form.errors.items():
                errors[field] = field_errors[0]  # 最初のエラーのみ表示
    return False, form, errors


def profile_update_validation(request):
    """
    プロフィール更新の入力値バリデーション
    :param request: Flaskのリクエストオブジェクト
    :return: (フラグ, フォーム, エラー)
    """
    form = ProfileUpdateForm(request.form)
    errors = {}
    if request.method == 'POST':
        if form.validate():
            return True, form, errors
        else:
            for field, field_errors in form.errors.items():
                errors[field] = field_errors[0]  # 最初のエラーのみ表示
    return False, form, errors


def password_change_validation(request):
    """
    パスワード変更の入力値バリデーション
    :param request: Flaskのリクエストオブジェクト
    :return: (フラグ, フォーム, エラー)
    """
    form = PasswordChangeForm(request.form)
    errors = {}
    if request.method == 'POST':
        if form.validate():
            return True, form, errors
        else:
            for field, field_errors in form.errors.items():
                errors[field] = field_errors[0]
    return False, form, errors


from sqlalchemy.exc import IntegrityError
import html
import os
import base64
import uuid
try:
    from PIL import Image
except ImportError:
    Image = None
from io import BytesIO

class AuthService:
    @staticmethod
    def create_user(username, email, password):
        """ユーザー作成処理（バリデーション済みデータを前提）"""
        try:
            # 重複チェック（データベースレベルでの最終確認）
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()

            if existing_user:
                if existing_user.username == username:
                    return False, ['このユーザー名は既に使用されています']
                if existing_user.email == email:
                    return False, ['このメールアドレスは既に使用されています']

            # ユーザー作成
            try:
                new_user = User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(password),
                    display_name=username
                )
                # 明示的にデフォルト値を設定しない（データベースのデフォルトを使用）

                db.session.add(new_user)
                db.session.flush()  # まずflushしてエラーを早期発見
                db.session.commit()

                return True, new_user
            except Exception as create_error:
                raise create_error

        except IntegrityError as e:
            db.session.rollback()
            return False, ['ユーザー名またはメールアドレスが既に使用されています']
        except Exception as e:
            db.session.rollback()
            return False, ['システムエラーが発生しました']

    @staticmethod
    def authenticate_user(username_or_email, password):
        """ユーザー認証処理"""
        try:
            user = User.query.filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()

            if user and user.check_password(password):
                return user
            return None

        except Exception as e:
            return None

    @staticmethod
    def handle_registration_form_back(request):
        """登録画面での「修正」ボタン処理"""
        form = RegistForm()
        # フォームに値を再設定（パスワード以外）- XSS対策でエスケープ
        username = html.escape(request.form.get('username', ''))
        email = html.escape(request.form.get('email', ''))
        form.username.data = username
        form.email.data = email
        form.password.data = ''  # パスワードは空にする
        return form

    @staticmethod
    def handle_registration_confirm(username, email, password):
        """登録確認処理"""
        # 必要な値が不足している場合はFalseを返す
        if not username or not email or not password:
            return False, 'error', '入力データが不足しています。再度入力してください。'

        # 登録処理を実行
        try:
            success, result = AuthService.create_user(username, email, password)

            if success:
                return True, 'success', 'アカウント登録が完了しました！'
            else:
                return False, 'error', '登録に失敗しました。入力内容をご確認ください。'
        except Exception as e:
            # データベースエラーなどの場合
            return False, 'error', 'システムエラーが発生しました。しばらく経ってから再度お試しください。'

    @staticmethod
    def handle_auto_login_after_registration(username, email):
        """登録後の自動ログイン処理"""
        if not username or not email:
            return False, 'error', 'セッションの有効期限が切れました。再度ログインしてください。'

        try:
            # データベースから直接ユーザー情報を取得
            user_obj = User.query.filter(User.username == username).first()

            if user_obj:
                # セッションにユーザー情報を保存（自動ログイン）
                session['user_id'] = user_obj.id
                session['username'] = user_obj.username
                session['is_logged_in'] = True
                # 登録用のセッション情報をクリア
                session.pop('registered_username', None)
                session.pop('registered_email', None)
                return True, 'success', f'ようこそ、{username}さん！チャットを始めましょう。'
            else:
                return False, 'error', 'ユーザー情報が見つかりませんでした。手動でログインしてください。'
        except Exception as e:
            return False, 'error', 'エラーが発生しました。手動でログインしてください。'

    @staticmethod
    def logout_user():
        """ログアウト処理 - 全てのセッション情報を削除"""
        session.clear()  # 全てのセッション情報を削除

    @staticmethod
    def allowed_file(filename):
        """アップロード可能なファイル形式をチェック"""
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def handle_profile_image_upload(user, cropped_image_data=None, file_data=None):
        """プロフィール画像アップロード処理"""
        try:
            if cropped_image_data:
                # Base64データから画像を保存
                # Base64ヘッダーを除去
                if ',' in cropped_image_data:
                    cropped_image_data = cropped_image_data.split(',')[1]

                # Base64デコード
                image_data = base64.b64decode(cropped_image_data)

                # ファイルサイズチェック（10MB）
                if len(image_data) > 10 * 1024 * 1024:  # 10MB
                    return False, 'ファイルサイズは10MB以下にしてください'

                try:
                    # 画像として読み込み
                    if Image is None:
                        return False, 'PIL(Pillow)ライブラリが必要です'
                    image = Image.open(BytesIO(image_data))
                except ImportError:
                    return False, 'PIL(Pillow)ライブラリが必要です'

                # ファイル名を生成
                filename = f"{uuid.uuid4()}.jpg"

                # アップロードディレクトリを作成
                upload_dir = os.path.join('app', 'static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)

                file_path = os.path.join(upload_dir, filename)

                # JPEGで保存
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(file_path, 'JPEG', quality=90)

                # 古い画像ファイルを削除
                if user.profile_image:
                    old_path = os.path.join(upload_dir, user.profile_image)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                user.profile_image = filename
                return True, '画像がアップロードされました'

            elif file_data and file_data.filename:
                # 通常のファイルアップロード（クロップなし）
                if AuthService.allowed_file(file_data.filename):
                    # ファイルサイズチェック（10MB）
                    file_data.seek(0, 2)  # ファイルの末尾に移動
                    file_size = file_data.tell()
                    file_data.seek(0)  # ファイルの先頭に戻す

                    if file_size > 10 * 1024 * 1024:  # 10MB
                        return False, 'ファイルサイズは10MB以下にしてください'

                    filename = secure_filename(file_data.filename)
                    # ファイル名をユニークにする
                    filename = f"{uuid.uuid4()}_{filename}"

                    # アップロードディレクトリを作成
                    upload_dir = os.path.join('app', 'static', 'uploads')
                    os.makedirs(upload_dir, exist_ok=True)

                    file_path = os.path.join(upload_dir, filename)
                    file_data.save(file_path)

                    # 古い画像ファイルを削除
                    if user.profile_image:
                        old_path = os.path.join(upload_dir, user.profile_image)
                        if os.path.exists(old_path):
                            os.remove(old_path)

                    user.profile_image = filename
                    return True, '画像がアップロードされました'

            return False, '有効な画像データが見つかりませんでした'

        except Exception as e:
            return False, f'画像の更新中にエラーが発生しました: {str(e)}'

    @staticmethod
    def update_user_profile(user, form):
        """ユーザープロフィール更新処理"""
        try:
            user.username = form.username.data
            user.display_name = form.display_name.data
            user.email = form.email.data
            user.bio = form.bio.data
            user.status = form.status.data
            user.status_message = form.status_message.data

            db.session.commit()

            # セッションのユーザー名も更新
            session['username'] = user.username
            return True, '設定が更新されました'

        except Exception as e:
            db.session.rollback()
            return False, '設定の更新中にエラーが発生しました'

    @staticmethod
    def change_user_password(user, current_password, new_password):
        """ユーザーパスワード変更処理"""
        # 現在のパスワード確認
        if not check_password_hash(user.password_hash, current_password):
            return False, '現在のパスワードが正しくありません'

        try:
            # パスワードを更新
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            return True, 'パスワードが変更されました'

        except Exception as e:
            db.session.rollback()
            return False, 'パスワード変更中にエラーが発生しました'

    @staticmethod
    def get_user_by_id(user_id):
        """IDでユーザーを取得"""
        return User.query.get(user_id)

    @staticmethod
    def setup_profile_form(user):
        """設定画面用のフォーム初期化"""
        form = ProfileUpdateForm()
        password_form = PasswordChangeForm()

        # フォームにデフォルト値を設定
        form.username.data = user.username
        form.display_name.data = user.display_name or user.username
        form.email.data = user.email
        form.bio.data = user.bio or ''
        form.status.data = user.status or 'online'
        form.status_message.data = user.status_message or ''

        return form, password_form

    @staticmethod
    def handle_profile_update(user, request):
        """プロフィール更新全体の処理"""
        form = ProfileUpdateForm()
        password_form = PasswordChangeForm()

        # プロフィール画像のみの更新チェック
        cropped_image_data = request.form.get('cropped_image_data')
        image_only_update = bool(cropped_image_data) and not any([
            request.form.get('username'),
            request.form.get('display_name'),
            request.form.get('email'),
            request.form.get('bio'),
            request.form.get('status'),
            request.form.get('status_message')
        ])

        if image_only_update:
            # 画像のみの更新処理
            success, message = AuthService.handle_profile_image_upload(user, cropped_image_data=cropped_image_data)
            if success:
                db.session.commit()
                return True, 'success', 'プロフィール画像を更新しました'
            else:
                db.session.rollback()
                return False, 'error', message

        # 通常のフォーム更新処理
        success, form, errors = profile_update_validation(request)

        if success:
            try:
                # プロフィール画像のアップロード処理
                cropped_image_data = request.form.get('cropped_image_data')
                if cropped_image_data:
                    img_success, img_message = AuthService.handle_profile_image_upload(
                        user, cropped_image_data=cropped_image_data
                    )
                    if not img_success:
                        return False, 'error', img_message

                elif form.profile_image.data:
                    # 通常のファイルアップロード（クロップなし）
                    img_success, img_message = AuthService.handle_profile_image_upload(
                        user, file_data=form.profile_image.data
                    )
                    if not img_success:
                        return False, 'error', img_message

                # フォームデータで更新
                profile_success, profile_message = AuthService.update_user_profile(user, form)
                if profile_success:
                    return True, 'success', profile_message
                else:
                    return False, 'error', profile_message

            except Exception as e:
                db.session.rollback()
                return False, 'error', '設定の更新中にエラーが発生しました'
        else:
            return False, 'validation_error', errors

def register_user_service(username, email, password):
    """
    ユーザー登録処理（コントローラー向けラッパー）
    :param username: ユーザー名
    :param email: メールアドレス
    :param password: パスワード
    :return: 登録成功フラグ
    """
    success, result = AuthService.create_user(username, email, password)
    return success


def auth_user(username_or_email, password):
    """
    ユーザー認証処理（AuthServiceを使用）
    :param username_or_email: ユーザー名またはメールアドレス
    :param password: パスワード
    :return: ユーザー情報またはNone
    """
    user = AuthService.authenticate_user(username_or_email, password)
    if user:
        # SQLAlchemy結果をdictライクオブジェクトに変換
        class UserResult:
            def __init__(self, user):
                self.user_id = user.id
                self.username = user.username
                self.email = user.email
                self.role = user.role  # ロール情報を追加
                self.user_status = user.status
        return UserResult(user)
    return None
