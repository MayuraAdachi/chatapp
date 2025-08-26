# ユーザー認証（登録・ログイン・ログアウト）
from flask import render_template, request, redirect, url_for, session, flash
from app.forms.regist_form import RegistForm
from app.forms.login_form import LoginForm
from app.forms.password_change_form import PasswordChangeForm
from app.forms.profile_update_form import ProfileUpdateForm
from app.services.auth_service import (
    regist_validation, login_validation, auth_user, register_user_service,
    profile_update_validation, password_change_validation, AuthService
)
import html

def index():
    """
    トップページ（ログイン画面）
    """
    form = LoginForm()
    return render_template('auth/login.html', form=form)

def regist():
    """
    登録画面表示・確認画面へ遷移
    GET: 登録画面
    POST: 確認画面へ遷移・確認画面からの修正処理
    """
    form = RegistForm()

    if request.method == 'POST':
        # 確認画面からの修正の場合
        if request.form.get('back_to_form'):
            form = AuthService.handle_registration_form_back(request)
            return render_template('auth/regist.html', form=form)

        # 通常の登録処理
        success, form, errors = regist_validation(request)
        if success:
            # 入力値を確認画面に渡す
            username = html.escape(form.username.data)
            email = html.escape(form.email.data)
            password = form.password.data
            return render_template('auth/regist_confirm.html', username=username, email=email, password=password)

        # バリデーションエラーがあればフォームに戻す
        return render_template('auth/regist.html', form=form, errors=errors)

    return render_template('auth/regist.html', form=form)


def regist_confirm():
    """
    確認画面の表示・完了画面へ遷移
    POST: 完了画面
    GET: 戻る（登録フォーム）
    """
    if request.method == 'POST':
        # XSS対策: フォームデータをサニタイズ
        username = html.escape(request.form.get('username', ''))
        email = html.escape(request.form.get('email', ''))
        password = request.form.get('password', '')

        # 登録処理を実行
        success, msg_type, message = AuthService.handle_registration_confirm(username, email, password)

        if success:
            # 登録成功時 → 完了画面へ
            session['registered_username'] = username
            session['registered_email'] = email
            flash(message, 'success')
            return redirect(url_for('auth.regist_complete'))
        else:
            flash(message, 'error')
            return redirect(url_for('auth.regist'))

    # GETリクエストの場合は登録画面にリダイレクト
    return redirect(url_for('auth.regist'))


def regist_complete():
    """
    完了画面の表示・自動ログイン処理
    GET: 登録完了画面を表示
    POST: 自動ログインしてroom一覧へ
    """
    if request.method == 'POST':
        # 自動ログイン処理
        username = session.get('registered_username')
        email = session.get('registered_email')

        success, msg_type, message = AuthService.handle_auto_login_after_registration(username, email)

        if success:
            flash(message, 'success')
            return redirect(url_for('room.index'))
        else:
            flash(message, 'error')
            return redirect(url_for('auth.login'))

    # GET: 完了画面を表示
    username = session.get('registered_username', 'ゲスト')
    return render_template('auth/regist_complete.html', username=username)

def login():
    """
    ログインフォーム表示・認証処理
    GET: ログインフォームを表示
    POST: サービス層で認証し、成功時はルーム一覧へ
    """
    form = LoginForm()

    if request.method == 'POST':
        # バリデーション実行
        success, form, errors = login_validation(request)

        if success:
            # XSS対策: フォームデータをサニタイズ
            username_or_email = html.escape(request.form.get('username', ''))
            password = request.form.get('password', '')  # パスワードはハッシュ化されるのでエスケープ不要

            # 認証処理を実行
            user = auth_user(username_or_email, password)
            if user:
                # セッションにユーザー情報を保存
                session['user_id'] = user.user_id
                session['username'] = user.username
                session['role'] = user.role  # ユーザーのロール情報を追加
                session['is_logged_in'] = True
                return redirect(url_for('room.index'))
            else:
                errors['username'] = 'ユーザー名またはメールアドレス、またはパスワードが間違っています'

        # バリデーションエラーまたは認証エラーがあればフォームに戻す
        return render_template('auth/login.html', form=form, errors=errors)

    return render_template('auth/login.html', form=form)


def logout():
    """
    ログアウト処理
    セッションを破棄し、トップページへリダイレクト
    """
    # 既存のフラッシュメッセージを全て削除
    session.pop('_flashes', None)

    # ログアウト処理を実行
    AuthService.logout_user()

    # ログアウトメッセージのみを表示
    flash('ログアウトしました', 'info')
    return redirect(url_for('main.index'))

def settings():
    """
    設定画面表示・更新処理
    GET: 設定画面を表示
    POST: 設定を更新
    """
    # ログイン状態チェック
    user_id = session.get('user_id')
    if not user_id:
        flash('ログインが必要です', 'error')
        return redirect(url_for('auth.login'))

    user = AuthService.get_user_by_id(user_id)
    if not user:
        flash('ユーザー情報が見つかりません', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        # フォームにデフォルト値を設定
        form, password_form = AuthService.setup_profile_form(user)
        return render_template('auth/settings.html', user=user, form=form, password_form=password_form, errors={})

    if request.method == 'POST':
        # プロフィール更新処理
        success, msg_type, message = AuthService.handle_profile_update(user, request)

        if success:
            flash(message, 'success')
            return redirect(url_for('auth.settings'))
        elif msg_type == 'validation_error':
            # バリデーションエラーの場合はフォームを再表示
            form, password_form = AuthService.setup_profile_form(user)
            return render_template('auth/settings.html', user=user, form=form, password_form=password_form, errors=message)
        else:
            flash(message, 'error')
            form, password_form = AuthService.setup_profile_form(user)
            return render_template('auth/settings.html', user=user, form=form, password_form=password_form, errors={})

    form, password_form = AuthService.setup_profile_form(user)
    return render_template('auth/settings.html', user=user, form=form, password_form=password_form, errors={})

def change_password():
    """
    パスワード変更処理
    """
    # ログイン状態チェック
    user_id = session.get('user_id')
    if not user_id:
        flash('ログインが必要です', 'error')
        return redirect(url_for('auth.login'))

    user = AuthService.get_user_by_id(user_id)
    if not user:
        flash('ユーザー情報が見つかりません', 'error')
        return redirect(url_for('auth.login'))

    # バリデーション実行
    success, form, errors = password_change_validation(request)

    if not success:
        # バリデーションエラーの場合
        for field, error in errors.items():
            flash(error, 'error')
        return redirect(url_for('auth.settings'))

    # パスワード変更処理
    success, message = AuthService.change_user_password(
        user,
        form.current_password.data,
        form.new_password.data
    )

    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')

    return redirect(url_for('auth.settings'))
