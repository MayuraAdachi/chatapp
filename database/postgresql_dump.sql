-- ===================================================
-- データベース作成
-- PostgreSQL用 DDL
-- ===================================================

-- 既存テーブルを全部消す（開発用。消したくないときはコメントアウト）
-- マスタテーブル
DROP TABLE IF EXISTS m_user_roles CASCADE;
DROP TABLE IF EXISTS m_user_statuses CASCADE;
DROP TABLE IF EXISTS m_room_types CASCADE;
DROP TABLE IF EXISTS m_message_types CASCADE;
DROP TABLE IF EXISTS m_room_roles CASCADE;
DROP TABLE IF EXISTS m_languages CASCADE;
-- トランザクションテーブル
DROP TABLE IF EXISTS t_messages CASCADE;
DROP TABLE IF EXISTS t_room_members CASCADE;
DROP TABLE IF EXISTS t_rooms CASCADE;
DROP TABLE IF EXISTS t_sessions CASCADE;
DROP TABLE IF EXISTS t_users CASCADE;

-- 部屋名検索用とパスワードハッシュ用の拡張を有効化
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- 部屋名検索でLIKE高速化
CREATE EXTENSION IF NOT EXISTS pgcrypto; -- パスワード暗号化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- UUID生成

-- ===================================================
-- マスタテーブル作成
-- ===================================================

-- 1. ロールマスタ
CREATE TABLE m_user_roles (
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

-- m_user_rolesテーブル論理名コメント
COMMENT ON TABLE m_user_roles IS 'ユーザーロールマスタ（権限管理）';
COMMENT ON COLUMN m_user_roles.id IS 'ロールID';
COMMENT ON COLUMN m_user_roles.role_code IS 'ロールコード';
COMMENT ON COLUMN m_user_roles.role_name IS 'ロール表示名';
COMMENT ON COLUMN m_user_roles.description IS '権限説明';
COMMENT ON COLUMN m_user_roles.can_edit_master IS '全マスタ編集権限';
COMMENT ON COLUMN m_user_roles.can_edit_user IS 'ユーザー情報編集権限';
COMMENT ON COLUMN m_user_roles.can_view_master IS 'マスタ閲覧権限';
COMMENT ON COLUMN m_user_roles.can_view_user IS 'ユーザー情報閲覧権限';
COMMENT ON COLUMN m_user_roles.display_order IS '表示順';
COMMENT ON COLUMN m_user_roles.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN m_user_roles.is_active IS '有効フラグ';
COMMENT ON COLUMN m_user_roles.created_at IS '作成日時';
COMMENT ON COLUMN m_user_roles.updated_at IS '更新日時';

-- 2. ステータスマスタ
CREATE TABLE m_user_statuses (
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

-- m_user_statusesテーブル論理名コメント
COMMENT ON TABLE m_user_statuses IS 'ユーザーステータスマスタ';
COMMENT ON COLUMN m_user_statuses.id IS 'ステータスID';
COMMENT ON COLUMN m_user_statuses.status_code IS 'ステータスコード（online, offline, away, busy, invisible等）';
COMMENT ON COLUMN m_user_statuses.status_name IS 'ステータス表示名';
COMMENT ON COLUMN m_user_statuses.description IS '説明';
COMMENT ON COLUMN m_user_statuses.display_order IS '表示順';
COMMENT ON COLUMN m_user_statuses.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN m_user_statuses.is_active IS '有効フラグ';
COMMENT ON COLUMN m_user_statuses.created_at IS '作成日時';
COMMENT ON COLUMN m_user_statuses.updated_at IS '更新日時';

-- 3. ルームタイプマスタ
CREATE TABLE m_room_types (
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

-- m_room_typesテーブル論理名コメント
COMMENT ON TABLE m_room_types IS 'ルームタイプマスタ';
COMMENT ON COLUMN m_room_types.id IS 'タイプID';
COMMENT ON COLUMN m_room_types.type_code IS 'タイプコード（group, one_on_one, support等）';
COMMENT ON COLUMN m_room_types.type_name IS 'タイプ表示名';
COMMENT ON COLUMN m_room_types.description IS '説明';
COMMENT ON COLUMN m_room_types.display_order IS '表示順';
COMMENT ON COLUMN m_room_types.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN m_room_types.is_active IS '有効フラグ';
COMMENT ON COLUMN m_room_types.created_at IS '作成日時';
COMMENT ON COLUMN m_room_types.updated_at IS '更新日時';

-- 4. メッセージタイプマスタ
CREATE TABLE m_message_types (
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

-- m_message_typesテーブル論理名コメント
COMMENT ON TABLE m_message_types IS 'メッセージタイプマスタ';
COMMENT ON COLUMN m_message_types.id IS 'タイプID';
COMMENT ON COLUMN m_message_types.type_code IS 'タイプコード（text, system, image, file等）';
COMMENT ON COLUMN m_message_types.type_name IS 'タイプ表示名';
COMMENT ON COLUMN m_message_types.description IS '説明';
COMMENT ON COLUMN m_message_types.display_order IS '表示順';
COMMENT ON COLUMN m_message_types.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN m_message_types.is_active IS '有効フラグ';
COMMENT ON COLUMN m_message_types.created_at IS '作成日時';
COMMENT ON COLUMN m_message_types.updated_at IS '更新日時';

-- 5. ルーム内ロールマスタ
CREATE TABLE m_room_roles (
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

-- m_room_rolesテーブル論理名コメント
COMMENT ON TABLE m_room_roles IS 'ルーム内ロールマスタ';
COMMENT ON COLUMN m_room_roles.id IS 'ロールID';
COMMENT ON COLUMN m_room_roles.role_code IS 'ロールコード';
COMMENT ON COLUMN m_room_roles.role_name IS 'ロール表示名';
COMMENT ON COLUMN m_room_roles.description IS '説明';
COMMENT ON COLUMN m_room_roles.can_invite IS 'メンバー招待権限';
COMMENT ON COLUMN m_room_roles.can_kick IS 'メンバー追放権限';
COMMENT ON COLUMN m_room_roles.can_edit_room IS 'ルーム設定編集権限';
COMMENT ON COLUMN m_room_roles.can_delete_messages IS 'メッセージ削除権限';
COMMENT ON COLUMN m_room_roles.display_order IS '表示順';
COMMENT ON COLUMN m_room_roles.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN m_room_roles.is_active IS '有効フラグ';
COMMENT ON COLUMN m_room_roles.created_at IS '作成日時';
COMMENT ON COLUMN m_room_roles.updated_at IS '更新日時';

-- 6. 言語マスタ
CREATE TABLE m_languages (
    id SERIAL PRIMARY KEY,
    lang_code VARCHAR(10) UNIQUE NOT NULL,
    lang_name VARCHAR(50) NOT NULL,        -- 表示名
    display_order INTEGER DEFAULT 0,      -- 表示順
    is_system BOOLEAN DEFAULT FALSE,       -- システム定義フラグ（削除不可）
    is_active BOOLEAN DEFAULT TRUE,        -- 有効フラグ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- m_languagesテーブル論理名コメント
COMMENT ON TABLE m_languages IS '言語マスタ';
COMMENT ON COLUMN m_languages.id IS '言語ID';
COMMENT ON COLUMN m_languages.lang_code IS '言語コード（ja, en, zh, ko等）';
COMMENT ON COLUMN m_languages.lang_name IS '言語表示名';
COMMENT ON COLUMN m_languages.display_order IS '表示順';
COMMENT ON COLUMN m_languages.is_system IS 'システム定義フラグ（削除不可）';
COMMENT ON COLUMN m_languages.is_active IS '有効フラグ';
COMMENT ON COLUMN m_languages.created_at IS '作成日時';
COMMENT ON COLUMN m_languages.updated_at IS '更新日時';

-- ===================================================
-- トランザクションテーブル作成
-- ===================================================

-- 1. ユーザーテーブル（登録ユーザー）
CREATE TABLE t_users (
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

-- t_usersテーブル論理名コメント
COMMENT ON TABLE t_users IS 'ユーザー情報';
COMMENT ON COLUMN t_users.id IS 'ユーザーID';
COMMENT ON COLUMN t_users.username IS 'ユーザー名（ログインID）';
COMMENT ON COLUMN t_users.email IS 'メールアドレス';
COMMENT ON COLUMN t_users.password_hash IS 'パスワードハッシュ（pgcrypto）';
COMMENT ON COLUMN t_users.display_name IS '表示名';
COMMENT ON COLUMN t_users.role IS 'ユーザーロール（画面で動的追加可能）';
COMMENT ON COLUMN t_users.avatar_url IS 'アバター画像URL';
COMMENT ON COLUMN t_users.profile_image IS 'プロフィール画像ファイル名';
COMMENT ON COLUMN t_users.bio IS '自己紹介';
COMMENT ON COLUMN t_users.status IS 'オンラインステータス（画面で動的追加可能）';
COMMENT ON COLUMN t_users.status_message IS 'ステータスメッセージ';
COMMENT ON COLUMN t_users.last_seen IS '最終アクセス日時';
COMMENT ON COLUMN t_users.created_at IS '作成日時';
COMMENT ON COLUMN t_users.updated_at IS '更新日時';

-- 2. セッションテーブル（匿名ユーザー管理）
CREATE TABLE t_sessions (
    id VARCHAR(255) PRIMARY KEY,
    display_name VARCHAR(100) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

-- t_sessionsテーブル論理名コメント
COMMENT ON TABLE t_sessions IS '匿名ユーザーのセッション情報';
COMMENT ON COLUMN t_sessions.id IS 'セッションID';
COMMENT ON COLUMN t_sessions.display_name IS '表示名（匿名ユーザー）';
COMMENT ON COLUMN t_sessions.ip_address IS 'IPアドレス';
COMMENT ON COLUMN t_sessions.user_agent IS 'ユーザーエージェント';
COMMENT ON COLUMN t_sessions.created_at IS '作成日時';
COMMENT ON COLUMN t_sessions.last_active IS '最終アクティブ日時';
COMMENT ON COLUMN t_sessions.expires_at IS '有効期限';

-- 3. ルームテーブル
CREATE TABLE t_rooms (
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

-- t_roomsテーブル論理名コメント
COMMENT ON TABLE t_rooms IS 'チャットルーム情報';
COMMENT ON COLUMN t_rooms.id IS 'ルームID';
COMMENT ON COLUMN t_rooms.name IS 'ルーム名';
COMMENT ON COLUMN t_rooms.description IS 'ルーム説明';
COMMENT ON COLUMN t_rooms.type IS 'ルームタイプ（画面で動的追加可能）';
COMMENT ON COLUMN t_rooms.is_private IS 'プライベートフラグ';
COMMENT ON COLUMN t_rooms.password_hash IS 'ルームパスワードハッシュ';
COMMENT ON COLUMN t_rooms.max_members IS '最大メンバー数';
COMMENT ON COLUMN t_rooms.created_by_user_id IS '作成者ユーザーID';
COMMENT ON COLUMN t_rooms.created_by_session IS '作成者セッションID';
COMMENT ON COLUMN t_rooms.created_by_name IS '作成者名（登録ユーザーはusername、匿名ユーザーは表示名）';
COMMENT ON COLUMN t_rooms.message_retention_days IS 'メッセージ保存日数';
COMMENT ON COLUMN t_rooms.max_message_count IS '最大メッセージ数';
COMMENT ON COLUMN t_rooms.created_at IS '作成日時';
COMMENT ON COLUMN t_rooms.updated_at IS '更新日時';

-- 4. ルームメンバーテーブル
CREATE TABLE t_room_members (
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

-- t_room_membersテーブル論理名コメント
COMMENT ON TABLE t_room_members IS 'ルームメンバー情報';
COMMENT ON COLUMN t_room_members.id IS 'ルームメンバーID';
COMMENT ON COLUMN t_room_members.room_id IS 'ルームID';
COMMENT ON COLUMN t_room_members.user_id IS 'ユーザーID（登録ユーザー）';
COMMENT ON COLUMN t_room_members.session_id IS 'セッションID（匿名ユーザー）';
COMMENT ON COLUMN t_room_members.display_name IS '表示名';
COMMENT ON COLUMN t_room_members.role IS 'ルーム内ロール（画面で動的追加可能）';
COMMENT ON COLUMN t_room_members.joined_at IS '参加日時';
COMMENT ON COLUMN t_room_members.last_active IS '最終アクティブ日時';

-- 5. メッセージテーブル
CREATE TABLE t_messages (
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

-- t_messagesテーブル論理名コメント
COMMENT ON TABLE t_messages IS 'チャットメッセージ情報';
COMMENT ON COLUMN t_messages.id IS 'メッセージID';
COMMENT ON COLUMN t_messages.room_id IS 'ルームID';
COMMENT ON COLUMN t_messages.user_id IS 'ユーザーID（登録ユーザー）';
COMMENT ON COLUMN t_messages.session_id IS 'セッションID（匿名ユーザー）';
COMMENT ON COLUMN t_messages.display_name IS '表示名';
COMMENT ON COLUMN t_messages.content IS 'メッセージ内容';
COMMENT ON COLUMN t_messages.message_type IS 'メッセージタイプ（画面で動的追加可能）';
COMMENT ON COLUMN t_messages.reply_to IS '返信先メッセージID';
COMMENT ON COLUMN t_messages.edited IS '編集済みフラグ';
COMMENT ON COLUMN t_messages.created_at IS '作成日時';
COMMENT ON COLUMN t_messages.updated_at IS '更新日時';

-- ===================================================
-- インデックス作成
-- ===================================================

-- マスタテーブル用インデックス
CREATE INDEX idx_m_user_roles_active ON m_user_roles(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_m_user_statuses_active ON m_user_statuses(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_m_room_types_active ON m_room_types(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_m_message_types_active ON m_message_types(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_m_room_roles_active ON m_room_roles(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_m_languages_active ON m_languages(is_active) WHERE is_active = TRUE;

-- ユーザー検索用
CREATE INDEX idx_t_users_username ON t_users(username);
CREATE INDEX idx_t_users_email ON t_users(email);
CREATE INDEX idx_t_users_role ON t_users(role);

-- セッション管理用
CREATE INDEX idx_t_sessions_expires ON t_sessions(expires_at);
CREATE INDEX idx_t_sessions_last_active ON t_sessions(last_active);

-- ルーム検索用（部屋名検索）
CREATE INDEX idx_t_rooms_name ON t_rooms USING gin(name gin_trgm_ops);
CREATE INDEX idx_t_rooms_created ON t_rooms(created_at DESC);
CREATE INDEX idx_t_rooms_type ON t_rooms(type);
CREATE INDEX idx_t_rooms_is_private ON t_rooms(is_private);

-- ルームメンバー検索用
CREATE INDEX idx_t_room_members_room ON t_room_members(room_id);
CREATE INDEX idx_t_room_members_user ON t_room_members(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_t_room_members_session ON t_room_members(session_id) WHERE session_id IS NOT NULL;
CREATE INDEX idx_t_room_members_last_active ON t_room_members(last_active DESC);

-- メッセージ検索用（最新順、300件制限に対応）
CREATE INDEX idx_t_messages_room_created ON t_messages(room_id, created_at DESC);
CREATE INDEX idx_t_messages_user ON t_messages(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_t_messages_session ON t_messages(session_id) WHERE session_id IS NOT NULL;
CREATE INDEX idx_t_messages_reply_to ON t_messages(reply_to) WHERE reply_to IS NOT NULL;

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
    (SELECT content FROM t_messages WHERE room_id = r.id ORDER BY created_at DESC LIMIT 1) as last_message
FROM t_rooms r
LEFT JOIN m_room_types rt ON r.type = rt.type_code AND rt.is_active = TRUE
LEFT JOIN t_room_members rm ON r.id = rm.room_id
LEFT JOIN t_messages m ON r.id = m.room_id
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
FROM t_messages m
LEFT JOIN m_message_types mt ON m.message_type = mt.type_code AND mt.is_active = TRUE
LEFT JOIN t_users u ON m.user_id = u.id
LEFT JOIN m_user_roles ur ON u.role = ur.role_code AND ur.is_active = TRUE
LEFT JOIN t_room_members rm ON (rm.room_id = m.room_id AND
    ((rm.user_id = m.user_id AND m.user_id IS NOT NULL) OR
     (rm.session_id = m.session_id AND m.session_id IS NOT NULL)))
LEFT JOIN m_room_roles rr ON rm.role = rr.role_code AND rr.is_active = TRUE;

-- ===================================================
-- スキーマ作成完了
-- ===================================================

-- 作成されたテーブルの確認
SELECT 'テーブル作成完了' as status, COUNT(*) || ' テーブル作成済み' as result
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
