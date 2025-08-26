# ルーム関連のWTFormsフォーム
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp, ValidationError
from app.models.room import get_rooms

class RoomCreateForm(FlaskForm):
    """ルーム作成フォーム"""
    room_name = StringField(
        'ルーム名',
        validators=[
            DataRequired(message='ルーム名は必須です'),
            Length(min=1, max=100, message='ルーム名は1〜100文字で入力してください')
        ]
    )

    room_description = TextAreaField(
        'ルーム説明',
        validators=[
            Optional(),
            Length(max=500, message='ルーム説明は500文字以内で入力してください')
        ]
    )

    max_members = IntegerField(
        '最大メンバー数',
        validators=[
            NumberRange(min=2, max=100, message='最大メンバー数は2〜100人の範囲で設定してください')
        ],
        default=50
    )

    room_password = PasswordField(
        'ルームパスワード',
        validators=[
            Optional(),
            Length(min=4, max=32, message='パスワードは4〜32文字で入力してください'),
            Regexp(r'^[a-zA-Z0-9]+$', message='パスワードは半角英数字のみ使用可能です')
        ]
    )

    def validate_room_name(self, field):
        """ルーム名の重複チェック"""
        if field.data:
            # 不正文字のチェック
            import re
            if not re.match(r'^[a-zA-Z0-9ぁ-んァ-ンー一-龯\s\-_()（）【】「」]+$', field.data):
                raise ValidationError('ルーム名に使用できない文字が含まれています')

            # 重複チェック
            existing_rooms = get_rooms()
            for room in existing_rooms:
                if room.name == field.data:
                    raise ValidationError('このルーム名は既に使用されています')

    def validate_max_members(self, field):
        """最大メンバー数の妥当性チェック"""
        if field.data is not None:
            try:
                max_members = int(field.data)
                if max_members < 2 or max_members > 100:
                    raise ValidationError('最大メンバー数は2〜100人の範囲で設定してください')
            except (ValueError, TypeError):
                raise ValidationError('最大メンバー数は数値で入力してください')

class AnonymousUserForm(FlaskForm):
    """匿名ユーザー登録フォーム"""
    username = StringField(
        'ユーザー名',
        validators=[
            DataRequired(message='ユーザー名は必須です'),
            Length(min=1, max=50, message='ユーザー名は1〜50文字で入力してください')
        ]
    )

class RoomJoinForm(FlaskForm):
    """ルーム参加フォーム"""
    password = PasswordField(
        'パスワード',
        validators=[
            Optional(),
            Length(min=4, max=32, message='パスワードは4〜32文字で入力してください')
        ]
    )
