-- ===================================================
-- データベース作成
-- PostgreSQL用 DDL（改良版）
-- 特徴：画面側で動的に区分値を追加可能、外部キー制約なし
-- ===================================================

-- 既存のENUM型削除（完全初期化用）
DROP TYPE IF EXISTS user_role_enum CASCADE;
DROP TYPE IF EXISTS user_status_enum CASCADE;
DROP TYPE IF EXISTS room_type_enum CASCADE;
DROP TYPE IF EXISTS message_type_enum CASCADE;
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS user_status CASCADE;
DROP TYPE IF EXISTS room_type CASCADE;
DROP TYPE IF EXISTS message_type CASCADE;

-- 既存テーブルを全部消す（開発用。消したくないときはコメントアウト）
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS room_members CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS user_roles CASCADE;
DROP TABLE IF EXISTS user_statuses CASCADE;
DROP TABLE IF EXISTS room_types CASCADE;
DROP TABLE IF EXISTS message_types CASCADE;
DROP TABLE IF EXISTS room_roles CASCADE;
DROP TABLE IF EXISTS languages CASCADE;

-- 部屋名検索用とパスワードハッシュ用の拡張を有効化
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- 部屋名検索でLIKE高速化
CREATE EXTENSION IF NOT EXISTS pgcrypto; -- パスワード暗号化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- UUID生成

-- ===================================================
-- マスタテーブル作成
-- ===================================================

-- 1. ロールマスタ
CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    role_code VARCHAR(20) UNIQUE NOT NULL,
    role_name VARCHAR(50) NOT NULL,        -- 表示名
    description TEXT,                      -- 権限説明
    can_edit_master BOOLEAN DEFAULT FALSE, -- 全マスタ編集可
    can_edit_user BOOLEAN DEFAULT FALSE,   -- ユーザー情報編集可
    can_view_master BOOLEAN DEFAULT FALSE, -- マスタ閲覧可
    can_view_user BOOLEAN DEFAULT FALSE,   -- ユーザー情報閲覧可
    display_order INTEGER DEFAULT 0,      -- 表示順
    is_system BOOLEAN DEFAULT FALSE,       -- システム定義フラグ（削除不可）
    is_active BOOLEAN DEFAULT TRUE,        -- 有効フラグ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- user_rolesテーブル論理名コメント
COMMENT ON TABLE user_roles IS 'ユーザーロールマスタ（権限管理）';
COMMENT ON COLUMN user_roles.id IS 'ロールID';
COMMENT ON COLUMN user_roles.role_code IS 'ロールコード';
COMMENT ON COLUMN user_roles.role_name IS 'ロール表示名';
COMMENT ON COLUMN user_roles.description IS '権限説明';
COMMENT ON COLUMN user_roles.can_edit_master IS '全マスタ編集権限';
COMMENT ON COLUMN user_roles.can_edit_user IS 'ユーザー情報編集権限';
COMMENT ON COLUMN user_roles.can_view_master IS 'マスタ閲覧権限';
COMMENT ON COLUMN user_roles.can_view_user IS 'ユーザー情報閲覧権限';
COMMENT ON COLUMN user_roles.display_order IS '表示順';
COMMENT ON COLUMN user_roles.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN user_roles.is_active IS '有効フラグ';
COMMENT ON COLUMN user_roles.created_at IS '作成日時';
COMMENT ON COLUMN user_roles.updated_at IS '更新日時';

-- 2. ステータスマスタ
CREATE TABLE user_statuses (
    id SERIAL PRIMARY KEY,
    status_code VARCHAR(20) UNIQUE NOT NULL,
    status_name VARCHAR(50) NOT NULL,        -- 表示名
    description TEXT,
    display_order INTEGER DEFAULT 0,
    is_system BOOLEAN DEFAULT FALSE,         -- システム定義フラグ（削除不可）
    is_active BOOLEAN DEFAULT TRUE,          -- 有効フラグ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- user_statusesテーブル論理名コメント
COMMENT ON TABLE user_statuses IS 'ユーザーステータスマスタ';
COMMENT ON COLUMN user_statuses.id IS 'ステータスID';
COMMENT ON COLUMN user_statuses.status_code IS 'ステータスコード（online, offline, away, busy, invisible等）';
COMMENT ON COLUMN user_statuses.status_name IS 'ステータス表示名';
COMMENT ON COLUMN user_statuses.description IS '説明';
COMMENT ON COLUMN user_statuses.display_order IS '表示順';
COMMENT ON COLUMN user_statuses.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN user_statuses.is_active IS '有効フラグ';
COMMENT ON COLUMN user_statuses.created_at IS '作成日時';
COMMENT ON COLUMN user_statuses.updated_at IS '更新日時';

-- 3. ルームタイプマスタ
CREATE TABLE room_types (
    id SERIAL PRIMARY KEY,
    type_code VARCHAR(20) UNIQUE NOT NULL,
    type_name VARCHAR(50) NOT NULL,        -- 表示名
    description TEXT,
    display_order INTEGER DEFAULT 0,      -- 表示順
    is_system BOOLEAN DEFAULT FALSE,       -- システム定義フラグ（削除不可）
    is_active BOOLEAN DEFAULT TRUE,        -- 有効フラグ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- room_typesテーブル論理名コメント
COMMENT ON TABLE room_types IS 'ルームタイプマスタ';
COMMENT ON COLUMN room_types.id IS 'タイプID';
COMMENT ON COLUMN room_types.type_code IS 'タイプコード（group, one_on_one, support等）';
COMMENT ON COLUMN room_types.type_name IS 'タイプ表示名';
COMMENT ON COLUMN room_types.description IS '説明';
COMMENT ON COLUMN room_types.display_order IS '表示順';
COMMENT ON COLUMN room_types.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN room_types.is_active IS '有効フラグ';
COMMENT ON COLUMN room_types.created_at IS '作成日時';
COMMENT ON COLUMN room_types.updated_at IS '更新日時';

-- 4. メッセージタイプマスタ
CREATE TABLE message_types (
    id SERIAL PRIMARY KEY,
    type_code VARCHAR(20) UNIQUE NOT NULL,
    type_name VARCHAR(50) NOT NULL,        -- 表示名
    description TEXT,
    display_order INTEGER DEFAULT 0,      -- 表示順
    is_system BOOLEAN DEFAULT FALSE,       -- システム定義フラグ（削除不可）
    is_active BOOLEAN DEFAULT TRUE,        -- 有効フラグ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- message_typesテーブル論理名コメント
COMMENT ON TABLE message_types IS 'メッセージタイプマスタ';
COMMENT ON COLUMN message_types.id IS 'タイプID';
COMMENT ON COLUMN message_types.type_code IS 'タイプコード（text, system, image, file等）';
COMMENT ON COLUMN message_types.type_name IS 'タイプ表示名';
COMMENT ON COLUMN message_types.description IS '説明';
COMMENT ON COLUMN message_types.display_order IS '表示順';
COMMENT ON COLUMN message_types.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN message_types.is_active IS '有効フラグ';
COMMENT ON COLUMN message_types.created_at IS '作成日時';
COMMENT ON COLUMN message_types.updated_at IS '更新日時';

-- 5. ルーム内ロールマスタ
CREATE TABLE room_roles (
    id SERIAL PRIMARY KEY,
    role_code VARCHAR(20) UNIQUE NOT NULL,
    role_name VARCHAR(50) NOT NULL,        -- 表示名
    description TEXT,
    can_invite BOOLEAN DEFAULT FALSE,      -- メンバー招待権限
    can_kick BOOLEAN DEFAULT FALSE,        -- メンバー追放権限
    can_edit_room BOOLEAN DEFAULT FALSE,   -- ルーム設定編集権限
    can_delete_messages BOOLEAN DEFAULT FALSE, -- メッセージ削除権限
    display_order INTEGER DEFAULT 0,      -- 表示順
    is_system BOOLEAN DEFAULT FALSE,       -- システム定義フラグ（削除不可）
    is_active BOOLEAN DEFAULT TRUE,        -- 有効フラグ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- room_rolesテーブル論理名コメント
COMMENT ON TABLE room_roles IS 'ルーム内ロールマスタ';
COMMENT ON COLUMN room_roles.id IS 'ロールID';
COMMENT ON COLUMN room_roles.role_code IS 'ロールコード';
COMMENT ON COLUMN room_roles.role_name IS 'ロール表示名';
COMMENT ON COLUMN room_roles.description IS '説明';
COMMENT ON COLUMN room_roles.can_invite IS 'メンバー招待権限';
COMMENT ON COLUMN room_roles.can_kick IS 'メンバー追放権限';
COMMENT ON COLUMN room_roles.can_edit_room IS 'ルーム設定編集権限';
COMMENT ON COLUMN room_roles.can_delete_messages IS 'メッセージ削除権限';
COMMENT ON COLUMN room_roles.display_order IS '表示順';
COMMENT ON COLUMN room_roles.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN room_roles.is_active IS '有効フラグ';
COMMENT ON COLUMN room_roles.created_at IS '作成日時';
COMMENT ON COLUMN room_roles.updated_at IS '更新日時';

-- 6. 言語マスタ
CREATE TABLE languages (
    id SERIAL PRIMARY KEY,
    lang_code VARCHAR(10) UNIQUE NOT NULL,
    lang_name VARCHAR(50) NOT NULL,        -- 表示名
    display_order INTEGER DEFAULT 0,      -- 表示順
    is_system BOOLEAN DEFAULT FALSE,       -- システム定義フラグ（削除不可）
    is_active BOOLEAN DEFAULT TRUE,        -- 有効フラグ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- languagesテーブル論理名コメント
COMMENT ON TABLE languages IS '言語マスタ';
COMMENT ON COLUMN languages.id IS '言語ID';
COMMENT ON COLUMN languages.lang_code IS '言語コード（ja, en, zh, ko等）';
COMMENT ON COLUMN languages.lang_name IS '言語表示名';
COMMENT ON COLUMN languages.display_order IS '表示順';
COMMENT ON COLUMN languages.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN languages.is_active IS '有効フラグ';
COMMENT ON COLUMN languages.created_at IS '作成日時';
COMMENT ON COLUMN languages.updated_at IS '更新日時';

-- ===================================================
-- メインテーブル作成
-- ===================================================

-- 1. ユーザーテーブル（登録ユーザー）
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- ユーザーID
    username VARCHAR(50) UNIQUE NOT NULL, -- ユーザー名
    email VARCHAR(100) UNIQUE NOT NULL, -- メールアドレス
    password_hash VARCHAR(255) NOT NULL, -- パスワードハッシュ
    display_name VARCHAR(100) NOT NULL, -- 表示名
    role VARCHAR(20) DEFAULT 'member', -- ロール
    avatar_url VARCHAR(255), -- アバター画像URL
    profile_image VARCHAR(255), -- プロフィール画像ファイル名
    bio TEXT, -- 自己紹介
    status VARCHAR(20) DEFAULT 'offline', -- ステータス
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
COMMENT ON COLUMN users.role IS 'ユーザーロール（画面で動的追加可能）';
COMMENT ON COLUMN users.avatar_url IS 'アバター画像URL';
COMMENT ON COLUMN users.profile_image IS 'プロフィール画像ファイル名';
COMMENT ON COLUMN users.bio IS '自己紹介';
COMMENT ON COLUMN users.status IS 'オンラインステータス（画面で動的追加可能）';
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
    type VARCHAR(20) DEFAULT 'group', -- ルームタイプ
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

    -- 作成者は登録ユーザーか匿名ユーザーのどちらか必須
    CONSTRAINT check_creator
        CHECK (created_by_user_id IS NOT NULL OR created_by_session IS NOT NULL)
);

-- roomsテーブル論理名コメント
COMMENT ON TABLE rooms IS 'チャットルーム情報';
COMMENT ON COLUMN rooms.id IS 'ルームID';
COMMENT ON COLUMN rooms.name IS 'ルーム名';
COMMENT ON COLUMN rooms.description IS 'ルーム説明';
COMMENT ON COLUMN rooms.type IS 'ルームタイプ（画面で動的追加可能）';
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
    role VARCHAR(20) DEFAULT 'member', -- ルーム内ロール
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

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
COMMENT ON COLUMN room_members.role IS 'ルーム内ロール（画面で動的追加可能）';
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
    message_type VARCHAR(20) DEFAULT 'text', -- メッセージタイプ
    reply_to UUID,
    edited BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

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
COMMENT ON COLUMN messages.message_type IS 'メッセージタイプ（画面で動的追加可能）';
COMMENT ON COLUMN messages.reply_to IS '返信先メッセージID';
COMMENT ON COLUMN messages.edited IS '編集済みフラグ';
COMMENT ON COLUMN messages.created_at IS '作成日時';
COMMENT ON COLUMN messages.updated_at IS '更新日時';

-- ===================================================
-- インデックス作成
-- ===================================================

-- マスタテーブル用インデックス
CREATE INDEX idx_user_roles_active ON user_roles(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_user_statuses_active ON user_statuses(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_room_types_active ON room_types(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_message_types_active ON message_types(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_room_roles_active ON room_roles(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_languages_active ON languages(is_active) WHERE is_active = TRUE;

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
    rt.type_name as type_display_name,
    r.is_private,
    r.max_members,
    r.created_at,
    COUNT(DISTINCT rm.id) as member_count,
    MAX(m.created_at) as last_message_at,
    (SELECT content FROM messages WHERE room_id = r.id ORDER BY created_at DESC LIMIT 1) as last_message
FROM rooms r
LEFT JOIN room_types rt ON r.type = rt.type_code AND rt.is_active = TRUE
LEFT JOIN room_members rm ON r.id = rm.room_id
LEFT JOIN messages m ON r.id = m.room_id
GROUP BY r.id, r.name, r.description, r.type, rt.type_name, r.is_private, r.max_members, r.created_at;

-- メッセージ詳細ビュー（送信者情報付き）
CREATE VIEW message_detail_view AS
SELECT
    m.id,
    m.room_id,
    m.content,
    m.message_type,
    mt.type_name as message_type_display_name,
    m.reply_to,
    m.edited,
    m.created_at,
    m.display_name,
    CASE
        WHEN m.user_id IS NOT NULL THEN 'registered'
        ELSE 'anonymous'
    END as sender_type,
    u.role as user_role,
    ur.role_name as user_role_display_name,
    rm.role as room_role,
    rr.role_name as room_role_display_name
FROM messages m
LEFT JOIN message_types mt ON m.message_type = mt.type_code AND mt.is_active = TRUE
LEFT JOIN users u ON m.user_id = u.id
LEFT JOIN user_roles ur ON u.role = ur.role_code AND ur.is_active = TRUE
LEFT JOIN room_members rm ON (rm.room_id = m.room_id AND
    ((rm.user_id = m.user_id AND m.user_id IS NOT NULL) OR
     (rm.session_id = m.session_id AND m.session_id IS NOT NULL)))
LEFT JOIN room_roles rr ON rm.role = rr.role_code AND rr.is_active = TRUE;

-- ===================================================
-- スキーマ作成完了
-- ===================================================

-- 作成されたテーブルの確認
SELECT 'テーブル作成完了' as status, COUNT(*) || ' テーブル作成済み' as result
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
