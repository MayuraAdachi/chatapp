# ユーザー認証（登録・ログイン・ログアウト）
from flask import render_template, request, redirect, url_for, session, flash
from app.forms.register_form import RegisterForm
from app.services.auth_service import regist_validation

def index():
    """
    トップページの表示
    """
    print("indexに入った")
    return render_template('auth/login.html')

def regist():
    print("registに入った")
    """
    アカウント登録フォーム表示・入力受付・確認画面へ遷移
    GET: 登録フォームを表示
    POST: 入力値を確認画面へ渡す
    """
    form = RegisterForm()
    if request.method == 'POST':
        success, form, errors = regist_validation(request)

        if success:
            # 入力値を確認画面に渡す
            return render_template('auth/regist_confirm.html', username=form.username.data, email=form.email.data, password=form.password.data)

        # バリデーションエラーがあればフォームに戻す
        return render_template('auth/regist.html', form=form, errors=errors)

    return render_template('auth/regist.html', form=form, errors={})


def regist_confirm():
    """
    確認画面の表示・完了画面へ遷移
    POST: サービス層でバリデーション・登録実行。成功時は完了画面へリダイレクト
    """


def regist_complete():
    """
    完了画面の表示・登録処理
    GET: 登録完了メッセージを表示
    """

def login():
    """
    ログインフォーム表示・認証処理
    GET: ログインフォームを表示
    POST: サービス層で認証し、成功時はルーム一覧へ
    """
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     if auth_user(username, password):
    #         session['user_id'] = username
    #         flash('ログインしました')
    #         return redirect(url_for('room.index'))
    #     else:
    #         flash('ユーザー名またはパスワードが違います')
    # return render_template('login.html')


def logout():
    """
    ログアウト処理
    セッションを破棄し、ログイン画面へリダイレクト
    """
    # session.pop('user_id', None)
    # flash('ログアウトしました')
    # return redirect(url_for('auth.login'))
