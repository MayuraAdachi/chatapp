# チャットアプリ

リアルタイムチャット機能を持つWebアプリケーションです。Flask、Socket.IO、PostgreSQLを使用して構築されています。

## 主な機能

- **リアルタイムチャット**: WebSocketを使用した即座のメッセージ配信
- **ユーザー管理**: 登録ユーザーと匿名ユーザーの両方に対応
- **ルーム機能**: パブリック・プライベートルームの作成と管理
- **多言語対応**: 日本語・英語の切り替え可能
- **管理者機能**: ユーザー管理、システム統計、開発ツール
- **プロフィール管理**: アバター画像、自己紹介、ステータス設定

## プロジェクト構成

```
chatapp/
├── app/
│   ├── controllers/     # コントローラー（ビジネスロジック）
│   ├── models/         # データモデル
│   ├── routes/         # ルーティング定義
│   ├── forms/          # WTForms（フォームバリデーション）
│   ├── templates/      # Jinjaテンプレート
│   ├── static/         # CSS, JS, 画像ファイル
│   └── utils/          # ユーティリティ関数
├── database/           # データベース関連
│   ├── postgresql_dump.sql      # DDL（テーブル定義）
│   ├── insert_initial_data.sql  # 初期データ
│   └── README.md               # データベース管理ガイド
├── translations/       # 多言語対応ファイル
├── tmp/               # 一時スクリプト・マイグレーション
├── logs/              # ログファイル
├── requirements.txt   # Python依存関係
└── run.py            # アプリケーション起動
```

--------------------------------------------------

## 基本セットアップ

1. 必要なパッケージのインストール（初回のみ）:

   ```powershell
   pip install -r requirements.txt
   ```

2. .envファイルの作成・編集:

   - `env_example` をコピーして `.env` を作成し、DB接続情報やシークレットキーを設定

3. データベースセットアップ:

   ```powershell
   # PostgreSQLデータベース作成
   createdb chatapp_db

   # スキーマ作成（テーブル定義）
   psql -d chatapp_db -f database/postgresql_dump.sql

   # 初期データ投入（管理者・テストユーザー等）
   psql -d chatapp_db -f database/insert_initial_data.sql
   ```

   詳細は `database/README.md` を参照

4. アプリの起動:

   ```powershell
   python run.py
   ```

5. ブラウザで `http://localhost:5000` を開くとチャット画面が表示される。

## 多言語対応（国際化）

このアプリは日本語と英語に対応しています。

### 言語の切り替え
- 画面右上の地球儀アイコンから言語を選択できます
- URL パラメータで直接指定: `?lang=en` または `?lang=ja`

### 翻訳の管理

新しい翻訳を追加または更新する場合：

1. Flask-Babelのインストール（開発用）:
   ```powershell
   pip install Flask-Babel
   ```

2. 翻訳用メッセージの抽出:
   ```powershell
   python translations.py extract
   ```

3. 新しい言語の初期化（例：フランス語）:
   ```powershell
   python translations.py init
   # 言語コード入力: fr
   ```

4. 既存翻訳の更新:
   ```powershell
   python translations.py update
   ```

5. 翻訳のコンパイル:
   ```powershell
   python translations.py compile
   ```

### サポート言語
- 日本語 (ja) - デフォルト
- 英語 (en)
