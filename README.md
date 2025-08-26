# チャットアプリの起動方法
--------------------------------------------------

1. 必要なパッケージのインストール（初回のみ）:

   ```powershell
   pip install -r requirements.txt
   ```

2. .envファイルの作成・編集:

   - `env_example` をコピーして `.env` を作成し、DB接続情報やシークレットキーを設定

3. PostgreSQLでデータベース・ユーザーを作成し、
   `database/chatapp_postgresql_dump.sql` を流し込む

4. アプリの起動:

   ```powershell
   python run.py
   ```

5. ブラウザで `http://localhost:5000` を開くとチャット画面が表示される。
