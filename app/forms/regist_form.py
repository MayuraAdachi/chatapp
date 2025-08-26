from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp

class RegistForm(FlaskForm):
    username = StringField('ユーザー名', validators=[
        DataRequired(message='ユーザー名は必須項目です。'),
        Length(max=50, message='ユーザー名は50文字以内で入力してください。'),
        Regexp(r'^[\w\sぁ-んァ-ヶ一-龠々ー]+$', message='ユーザー名は日本語・英数字・アンダースコアのみ使用できます。')
    ])
    password = PasswordField('パスワード', validators=[
        DataRequired(message='パスワードは必須項目です。'),
        Length(min=6, max=100, message='パスワードは6～100文字で入力してください。')
    ])
    email = StringField('メールアドレス', validators=[
        DataRequired(message='メールアドレスは必須項目です。'),
        Email(message='メールアドレスの形式が正しくありません。'),
        Length(max=100, message='メールアドレスは100文字以内で入力してください。')
    ])
