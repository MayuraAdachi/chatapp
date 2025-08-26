-- ===================================================
-- データベース作成
-- PostgreSQL用 DDL
-- ===================================================

-- 既存テーブルを全部消す（開発用。消したくないときはコメントアウト）
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS room_members CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ENUM型も消す（既にあったら）
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS user_status CASCADE;
DROP TYPE IF EXISTS room_type CASCADE;
DROP TYPE IF EXISTS member_role CASCADE;
DROP TYPE IF EXISTS message_type CASCADE;

-- 部屋名検索用とパスワードハッシュ用の拡張を有効化
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- 部屋名検索でLIKE高速化
CREATE EXTENSION IF NOT EXISTS pgcrypto; -- パスワード暗号化

-- ===================================================
-- ENUM型の定義
-- ===================================================

-- ユーザーロール（開発者・管理者・一般）
CREATE TYPE user_role AS ENUM ('developer', 'admin', 'member');

-- ユーザーステータス（オンライン・オフライン・離席・忙しい・非表示）
CREATE TYPE user_status AS ENUM ('online', 'offline', 'away', 'busy', 'invisible');

-- ルームタイプ（グループ・1対1）
CREATE TYPE room_type AS ENUM ('group', 'one_on_one');

-- ルーム内ロール（作成者・管理・メンバー）
CREATE TYPE member_role AS ENUM ('creator', 'admin', 'member');

-- メッセージタイプ（テキスト・システム通知）
CREATE TYPE message_type AS ENUM ('text', 'system');

-- ===================================================
-- テーブル作成
-- ===================================================

-- 1. ユーザーテーブル（登録ユーザー）
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- ユーザーID
    username VARCHAR(50) UNIQUE NOT NULL, -- ユーザー名
    email VARCHAR(100) UNIQUE NOT NULL, -- メールアドレス
    password_hash VARCHAR(255) NOT NULL, -- パスワードハッシュ
    display_name VARCHAR(100) NOT NULL, -- 表示名
    role user_role DEFAULT 'member', -- ロール
    avatar_url VARCHAR(255), -- アバター画像URL
    profile_image VARCHAR(255), -- プロフィール画像ファイル名
    bio TEXT, -- 自己紹介
    status user_status DEFAULT 'offline', -- ステータス
    status_message VARCHAR(100), -- ステータスメッセージ
    last_seen TIMESTAMP, -- 最終アクセス日時
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 作成日時
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 更新日時
);

-- usersテーブル論理名コメント
COMMENT ON TABLE users IS 'ユーザー情報';
COMMENT ON COLUMN users.id IS 'ユーザーID';
COMMENT ON COLUMN users.username IS 'ユーザー名（ログインID）';
COMMENT ON COLUMN users.email IS 'メールアドレス';
COMMENT ON COLUMN users.password_hash IS 'パスワードハッシュ（pgcrypto）';
COMMENT ON COLUMN users.display_name IS '表示名';
COMMENT ON COLUMN users.role IS 'ユーザーロール（developer/admin/member）';
COMMENT ON COLUMN users.avatar_url IS 'アバター画像URL';
COMMENT ON COLUMN users.profile_image IS 'プロフィール画像ファイル名';
COMMENT ON COLUMN users.bio IS '自己紹介';
COMMENT ON COLUMN users.status IS 'オンラインステータス';
COMMENT ON COLUMN users.status_message IS 'ステータスメッセージ';
COMMENT ON COLUMN users.last_seen IS '最終アクセス日時';
COMMENT ON COLUMN users.created_at IS '作成日時';
COMMENT ON COLUMN users.updated_at IS '更新日時';

-- 2. セッションテーブル（匿名ユーザー管理）
CREATE TABLE sessions (
    id VARCHAR(255) PRIMARY KEY,
    display_name VARCHAR(100) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

-- sessionsテーブル論理名コメント
COMMENT ON TABLE sessions IS '匿名ユーザーのセッション情報';
COMMENT ON COLUMN sessions.id IS 'セッションID';
COMMENT ON COLUMN sessions.display_name IS '表示名（匿名ユーザー）';
COMMENT ON COLUMN sessions.ip_address IS 'IPアドレス';
COMMENT ON COLUMN sessions.user_agent IS 'ユーザーエージェント';
COMMENT ON COLUMN sessions.created_at IS '作成日時';
COMMENT ON COLUMN sessions.last_active IS '最終アクティブ日時';
COMMENT ON COLUMN sessions.expires_at IS '有効期限';

-- 3. ルームテーブル
CREATE TABLE rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type room_type DEFAULT 'group',
    is_private BOOLEAN DEFAULT FALSE,
    password_hash VARCHAR(255),
    max_members INTEGER DEFAULT 50,
    created_by_user_id UUID,
    created_by_session VARCHAR(255),
    created_by_name VARCHAR(100),  -- 匿名ユーザー名を保存
    message_retention_days INTEGER DEFAULT 30,
    max_message_count INTEGER DEFAULT 300,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外部キー制約
    CONSTRAINT fk_rooms_created_by_user
        FOREIGN KEY (created_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_rooms_created_by_session
        FOREIGN KEY (created_by_session) REFERENCES sessions(id) ON DELETE SET NULL,

    -- 作成者は登録ユーザーか匿名ユーザーのどちらか必須
    CONSTRAINT check_creator
        CHECK (created_by_user_id IS NOT NULL OR created_by_session IS NOT NULL)
);

-- roomsテーブル論理名コメント
COMMENT ON TABLE rooms IS 'チャットルーム情報';
COMMENT ON COLUMN rooms.id IS 'ルームID';
COMMENT ON COLUMN rooms.name IS 'ルーム名';
COMMENT ON COLUMN rooms.description IS 'ルーム説明';
COMMENT ON COLUMN rooms.type IS 'ルームタイプ（group/one_on_one）';
COMMENT ON COLUMN rooms.is_private IS 'プライベートフラグ';
COMMENT ON COLUMN rooms.password_hash IS 'ルームパスワードハッシュ';
COMMENT ON COLUMN rooms.max_members IS '最大メンバー数';
COMMENT ON COLUMN rooms.created_by_user_id IS '作成者ユーザーID';
COMMENT ON COLUMN rooms.created_by_session IS '作成者セッションID';
COMMENT ON COLUMN rooms.created_by_name IS '作成者名（登録ユーザーはusername、匿名ユーザーは表示名）';
COMMENT ON COLUMN rooms.message_retention_days IS 'メッセージ保存日数';
COMMENT ON COLUMN rooms.max_message_count IS '最大メッセージ数';
COMMENT ON COLUMN rooms.created_at IS '作成日時';
COMMENT ON COLUMN rooms.updated_at IS '更新日時';

-- 4. ルームメンバーテーブル
CREATE TABLE room_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL,
    user_id UUID,
    session_id VARCHAR(255),
    display_name VARCHAR(100) NOT NULL,
    role member_role DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外部キー制約
    CONSTRAINT fk_room_members_room
        FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    CONSTRAINT fk_room_members_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_room_members_session
        FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,

    -- メンバーは登録ユーザーか匿名ユーザーのどちらか必須
    CONSTRAINT check_member
        CHECK (user_id IS NOT NULL OR session_id IS NOT NULL),

    -- 同一ルーム内でのユニーク制約
    CONSTRAINT unique_user_room
        UNIQUE (room_id, user_id),
    CONSTRAINT unique_session_room
        UNIQUE (room_id, session_id)
);

-- room_membersテーブル論理名コメント
COMMENT ON TABLE room_members IS 'ルームメンバー情報';
COMMENT ON COLUMN room_members.id IS 'ルームメンバーID';
COMMENT ON COLUMN room_members.room_id IS 'ルームID';
COMMENT ON COLUMN room_members.user_id IS 'ユーザーID（登録ユーザー）';
COMMENT ON COLUMN room_members.session_id IS 'セッションID（匿名ユーザー）';
COMMENT ON COLUMN room_members.display_name IS '表示名';
COMMENT ON COLUMN room_members.role IS 'ルーム内ロール';
COMMENT ON COLUMN room_members.joined_at IS '参加日時';
COMMENT ON COLUMN room_members.last_active IS '最終アクティブ日時';

-- 5. メッセージテーブル
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL,
    user_id UUID,
    session_id VARCHAR(255),
    display_name VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    message_type message_type DEFAULT 'text',
    reply_to UUID,
    edited BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外部キー制約
    CONSTRAINT fk_messages_room
        FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    CONSTRAINT fk_messages_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_messages_session
        FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE SET NULL,
    CONSTRAINT fk_messages_reply_to
        FOREIGN KEY (reply_to) REFERENCES messages(id) ON DELETE SET NULL,

    -- 送信者は登録ユーザーか匿名ユーザーのどちらか必須
    CONSTRAINT check_sender
        CHECK (user_id IS NOT NULL OR session_id IS NOT NULL)
);

-- messagesテーブル論理名コメント
COMMENT ON TABLE messages IS 'チャットメッセージ情報';
COMMENT ON COLUMN messages.id IS 'メッセージID';
COMMENT ON COLUMN messages.room_id IS 'ルームID';
COMMENT ON COLUMN messages.user_id IS 'ユーザーID（登録ユーザー）';
COMMENT ON COLUMN messages.session_id IS 'セッションID（匿名ユーザー）';
COMMENT ON COLUMN messages.display_name IS '表示名';
COMMENT ON COLUMN messages.content IS 'メッセージ内容';
COMMENT ON COLUMN messages.message_type IS 'メッセージタイプ（text/system）';
COMMENT ON COLUMN messages.reply_to IS '返信先メッセージID';
COMMENT ON COLUMN messages.edited IS '編集済みフラグ';
COMMENT ON COLUMN messages.created_at IS '作成日時';
COMMENT ON COLUMN messages.updated_at IS '更新日時';

-- ===================================================
-- インデックス作成
-- ===================================================

-- ユーザー検索用
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- セッション管理用
CREATE INDEX idx_sessions_expires ON sessions(expires_at);
CREATE INDEX idx_sessions_last_active ON sessions(last_active);

-- ルーム検索用（部屋名検索）
CREATE INDEX idx_rooms_name ON rooms USING gin(name gin_trgm_ops);
CREATE INDEX idx_rooms_created ON rooms(created_at DESC);
CREATE INDEX idx_rooms_type ON rooms(type);
CREATE INDEX idx_rooms_is_private ON rooms(is_private);

-- ルームメンバー検索用
CREATE INDEX idx_room_members_room ON room_members(room_id);
CREATE INDEX idx_room_members_user ON room_members(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_room_members_session ON room_members(session_id) WHERE session_id IS NOT NULL;
CREATE INDEX idx_room_members_last_active ON room_members(last_active DESC);

-- メッセージ検索用（最新順、300件制限に対応）
CREATE INDEX idx_messages_room_created ON messages(room_id, created_at DESC);
CREATE INDEX idx_messages_user ON messages(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_messages_session ON messages(session_id) WHERE session_id IS NOT NULL;
CREATE INDEX idx_messages_reply_to ON messages(reply_to) WHERE reply_to IS NOT NULL;

-- ===================================================
-- ビューの作成
-- ===================================================

-- ルーム一覧ビュー（メンバー数、最新メッセージ付き）
CREATE VIEW room_list_view AS
SELECT
    r.id,
    r.name,
    r.description,
    r.type,
    r.is_private,
    r.max_members,
    r.created_at,
    COUNT(DISTINCT rm.id) as member_count,
    MAX(m.created_at) as last_message_at,
    (SELECT content FROM messages WHERE room_id = r.id ORDER BY created_at DESC LIMIT 1) as last_message
FROM rooms r
LEFT JOIN room_members rm ON r.id = rm.room_id
LEFT JOIN messages m ON r.id = m.room_id
GROUP BY r.id, r.name, r.description, r.type, r.is_private, r.max_members, r.created_at;

-- メッセージ詳細ビュー（送信者情報付き）
CREATE VIEW message_detail_view AS
SELECT
    m.id,
    m.room_id,
    m.content,
    m.message_type,
    m.reply_to,
    m.edited,
    m.created_at,
    m.display_name,
    CASE
        WHEN m.user_id IS NOT NULL THEN 'registered'
        ELSE 'anonymous'
    END as sender_type,
    u.role as user_role,
    rm.role as room_role
FROM messages m
LEFT JOIN users u ON m.user_id = u.id
LEFT JOIN room_members rm ON (rm.room_id = m.room_id AND
    ((rm.user_id = m.user_id AND m.user_id IS NOT NULL) OR
     (rm.session_id = m.session_id AND m.session_id IS NOT NULL)));

-- ===================================================
-- スキーマ作成完了
-- ===================================================

-- 作成されたテーブルの確認
SELECT 'テーブル作成完了' as status, COUNT(*) || ' テーブル作成済み' as result
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
