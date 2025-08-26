# app/services/translation_service.py
"""
翻訳管理関連のビジネスロジックを提供するサービス層
"""
from app.utils.translation_helper import (
    get_available_languages,
    get_language_completion_status,
    save_custom_translation,
    BASIC_TRANSLATIONS
)
import json


class TranslationService:
    """翻訳管理サービス"""

    @staticmethod
    def get_language_admin_data():
        """言語管理画面用のデータを取得"""
        languages = get_available_languages()
        status = get_language_completion_status()
        return {
            'languages': languages,
            'status': status
        }

    @staticmethod
    def add_translation(lang, key, value):
        """翻訳追加処理"""
        if not lang or not key or not value:
            return False, 'すべての項目を入力してください'

        if save_custom_translation(lang, key, value):
            return True, f'翻訳を追加しました: {lang} - {key}'
        else:
            return False, '翻訳の保存に失敗しました'

    @staticmethod
    def export_translations(lang='en'):
        """翻訳データをJSON形式でエクスポート"""
        if lang in BASIC_TRANSLATIONS:
            return {
                'success': True,
                'data': {
                    'language': lang,
                    'translations': BASIC_TRANSLATIONS[lang]
                }
            }

        return {
            'success': False,
            'error': 'Language not found',
            'status_code': 404
        }
