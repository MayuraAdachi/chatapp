# app/utils/auto_translator.py
# 自動翻訳機能（GoogleTranslator使用）
import os
import json
from flask import current_app
from deep_translator import GoogleTranslator

class AutoTranslator:
    def __init__(self):
        self.cache = {}
        self.cache_file = 'translations_cache.json'
        # LibreTranslateのベースURL（参考用）
        self.libre_url = 'https://libretranslate.de'
        # 言語コードのマッピング（GoogleTranslator用）
        self.language_mapping = {
            'zh': 'zh',      # 中国語
            'zh-tw': 'zh',   # 中国語繁体字（LibreTranslateでは'zh'を使用）
            'ja': 'ja',      # 日本語
            'en': 'en',      # 英語
            'ko': 'ko',      # 韓国語
            'es': 'es',      # スペイン語
            'fr': 'fr',      # フランス語
            'de': 'de',      # ドイツ語
        }
        self.load_cache()

    def load_cache(self):
        """キャッシュファイルを読み込む"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
        except Exception as e:
            print(f"Cache load error: {e}")
            self.cache = {}

    def save_cache(self):
        """キャッシュをファイルに保存"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Cache save error: {e}")

    def get_cache_key(self, text, target_lang):
        """キャッシュキーを生成"""
        return f"{text}::{target_lang}"

    def translate_text(self, text, target_lang='en', source_lang='ja'):
        """テキストを翻訳する（キャッシュ付き）"""
        if target_lang == source_lang:
            return text

        # 言語コードをマッピング
        mapped_target_lang = self.language_mapping.get(target_lang, target_lang)
        mapped_source_lang = self.language_mapping.get(source_lang, source_lang)

        cache_key = self.get_cache_key(text, target_lang)

        # キャッシュから取得
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Deep Translatorで翻訳（Google Translate API使用）
            translator = GoogleTranslator(source=mapped_source_lang, target=mapped_target_lang)
            translated = translator.translate(text)

            # キャッシュに保存
            self.cache[cache_key] = translated
            self.save_cache()

            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # 翻訳失敗時は元のテキストを返す

    def translate_batch(self, texts, target_lang='en', source_lang='ja'):
        """複数のテキストを一括翻訳"""
        results = {}
        for text in texts:
            results[text] = self.translate_text(text, target_lang, source_lang)
        return results

# グローバルインスタンス
auto_translator = AutoTranslator()

def translate_auto(text, lang='en'):
    """自動翻訳関数"""
    return auto_translator.translate_text(text, target_lang=lang)
