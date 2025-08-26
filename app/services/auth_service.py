# ユーザー認証・登録関連のビジネスロジック
from app.models.user import regist_user, authenticate_user
from app.forms.register_form import RegisterForm

def regist_validation(request):
    """
    アカウント登録の入力値バリデーションと確認画面への遷移処理
    :param request: Flaskのリクエストオブジェクト
    :return: (成功フラグ, フォームオブジェクト, エラー辞書)
    """
    form = RegisterForm(request.form)
    print(form.data)
    errors = {}
    if request.method == 'POST':
        if form.validate():
            # 登録処理
            if regist_user(form.username.data, form.password.data, form.email.data):
                return True, form, errors
            else:
                errors['username'] = 'そのユーザー名またはメールアドレスは既に使われています。'
        else:
            for field, field_errors in form.errors.items():
                errors[field] = field_errors[0]  # 最初のエラーのみ表示
    return False, form, errors

def auth_user(username_or_email, password):
    if not username_or_email or not password:
        return False
    # ユーザー名またはメールアドレスで認証
    from sqlalchemy import text
    from app.extensions import db
    sql = text("""
        SELECT * FROM users WHERE (username=:ue OR email=:ue) AND password_hash=crypt(:password, password_hash)
    """)
    result = db.session.execute(sql, {'ue': username_or_email, 'password': password})
    return result.fetchone() is not None
