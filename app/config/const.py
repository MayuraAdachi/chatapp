"""
固定値で必要な定数を定義する
"""

APP_TITLE = "TransChat"
SUB_TITLE = "どの言語でも、すぐにつながる"
VERSION = "1.0.0"

# チャット関連
CHAT_LOG_DAYS = 3
CHAT_BACKUP_DAYS = 7
CSRF_TOKEN_EXPIRY = 3600 # CSRFトークンの有効期限（秒）

# 言語関連
SUPPORTED_LANGUAGES = {
    'ja': '日本語',
    'en': 'English',
    'zh': '中文',
    'ko': '한국어',
    'fr': 'Français',
    'de': 'Deutsch',
    'es': 'Español'
}
DEFAULT_LANGUAGE = 'ja'
DEFAULT_TIMEZONE = 'Asia/Tokyo'

# 優先対応言語（完全翻訳済み）
PRIORITY_LANGUAGES = ['ja']

# 開発中の言語（後で対応予定）
DEVELOPMENT_LANGUAGES = ['en', 'zh', 'ko', 'fr', 'de', 'es']
