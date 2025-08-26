from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('ユーザー名またはメールアドレス', validators=[
        DataRequired(message='ユーザー名またはメールアドレスは必須項目です。'),
        Length(max=100, message='ユーザー名またはメールアドレスは100文字以内で入力してください。')
    ])
    password = PasswordField('パスワード', validators=[
        DataRequired(message='パスワードは必須項目です。'),
        Length(max=100, message='パスワードは100文字以内で入力してください。')
    ])
