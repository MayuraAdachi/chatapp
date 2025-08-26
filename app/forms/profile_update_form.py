from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional, ValidationError

def validate_file_size(form, field):
    """ファイルサイズを10MBまでに制限"""
    if field.data:
        # ファイルサイズを取得
        field.data.seek(0, 2)  # ファイルの末尾に移動
        file_size = field.data.tell()
        field.data.seek(0)  # ファイルの先頭に戻す

        if file_size > 10 * 1024 * 1024:  # 10MB
            raise ValidationError('ファイルサイズは10MB以下にしてください。')

class ProfileUpdateForm(FlaskForm):
    profile_image = FileField('プロフィール画像', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='JPG、PNG、GIF形式のファイルのみアップロード可能です。'),
        validate_file_size
    ])

    username = StringField('ユーザー名', validators=[
        DataRequired(message='ユーザー名は必須項目です。'),
        Length(max=50, message='ユーザー名は50文字以内で入力してください。'),
        Regexp(r'^[\w\sぁ-んァ-ヶ一-龠々ー]+$', message='ユーザー名は日本語・英数字・アンダースコアのみ使用できます。')
    ])

    display_name = StringField('表示名', validators=[
        Optional(),
        Length(max=100, message='表示名は100文字以内で入力してください。')
    ])

    email = StringField('メールアドレス', validators=[
        DataRequired(message='メールアドレスは必須項目です。'),
        Email(message='メールアドレスの形式が正しくありません。'),
        Length(max=100, message='メールアドレスは100文字以内で入力してください。')
    ])

    bio = TextAreaField('自己紹介', validators=[
        Optional(),
        Length(max=500, message='自己紹介は500文字以内で入力してください。')
    ])

    status = SelectField('ステータス', choices=[
        ('online', 'オンライン'),
        ('away', '離席中'),
        ('busy', '取り込み中'),
        ('invisible', 'オフライン表示')
    ], validators=[DataRequired()])

    status_message = StringField('ステータスメッセージ', validators=[
        Optional(),
        Length(max=100, message='ステータスメッセージは100文字以内で入力してください。')
    ])
