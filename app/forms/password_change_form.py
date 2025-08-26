from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('現在のパスワード', validators=[
        DataRequired(message='現在のパスワードは必須項目です。')
    ])

    new_password = PasswordField('新しいパスワード', validators=[
        DataRequired(message='新しいパスワードは必須項目です。'),
        Length(min=6, max=100, message='パスワードは6～100文字で入力してください。')
    ])

    confirm_password = PasswordField('パスワード確認', validators=[
        DataRequired(message='パスワード確認は必須項目です。'),
        EqualTo('new_password', message='パスワードが一致しません。')
    ])
