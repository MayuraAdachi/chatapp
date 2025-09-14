#!/usr/bin/env python3
"""
DDL実行スクリプト
PostgreSQLのDDLファイルを実行してテーブルを再作成
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def run_ddl():
    """DDLファイルを実行"""
    # シンプルなFlaskアプリを作成
    app = Flask(__name__)

    # データベース設定（環境変数から取得、デフォルト値あり）
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'admin')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'chatapp_db')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)

    # DDLファイルのパス
    ddl_file = os.path.join(os.path.dirname(__file__), 'postgresql_dump.sql')

    with app.app_context():
        try:
            print("DDL実行中...")

            # DDLファイルを読み込み
            with open(ddl_file, 'r', encoding='utf-8') as f:
                ddl_content = f.read()

            # SQLを分割して実行（セミコロンで分割）
            sql_statements = [stmt.strip() for stmt in ddl_content.split(';') if stmt.strip()]

            for i, statement in enumerate(sql_statements):
                if statement:
                    try:
                        print(f"実行中: ステートメント {i+1}/{len(sql_statements)}")
                        db.session.execute(db.text(statement))
                        db.session.commit()
                    except Exception as e:
                        print(f"警告: ステートメント {i+1} でエラー: {e}")
                        db.session.rollback()
                        # DROP文やCREATE EXTENSION等のエラーは無視して続行
                        continue

            print("DDL実行完了!")
            return True

        except Exception as e:
            print(f"DDL実行エラー: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = run_ddl()
    if success:
        print("\n次に以下を実行してください:")
        print("python database/init_data.py")
        sys.exit(0)
    else:
        sys.exit(1)
