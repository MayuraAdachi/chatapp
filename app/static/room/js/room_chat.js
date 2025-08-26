// チャット画面用JavaScript - 完全版

let socket;
let typingTimer;
let isTyping = false;
let currentRoom = null;
let currentUser = null;

// ページ読み込み完了時の初期化
document.addEventListener('DOMContentLoaded', function() {
    console.log('チャット画面を初期化中...');

    // データの取得
    if (window.chatData) {
        currentRoom = {
            id: window.chatData.roomId,
            name: window.chatData.roomName,
            description: window.chatData.roomDescription
        };
        currentUser = {
            id: window.chatData.userId,
            name: window.chatData.username,
            isOwner: window.chatData.isOwner,
            isAdmin: window.chatData.isAdmin
        };
    } else {
        console.error('チャットデータが見つかりません');
        showToast('チャットデータの読み込みに失敗しました', 'danger');
        return;
    }

    // 初期化処理
    initializeSocket();
    setupMessageInput();
    setupUIEvents();
    joinRoom();
});

/**
 * Socket.IOの初期化
 */
function initializeSocket() {
    try {
        // Socket.IOが利用可能かチェック
        if (typeof io === 'undefined') {
            console.warn('Socket.IO が読み込まれていません。リアルタイム機能は無効です。');
            hideConnectingMessage();
            showToast('リアルタイム機能は無効です（表示のみ）', 'warning');
            return;
        }

        socket = io({
            transports: ['websocket', 'polling']
        });

        // 接続イベント
        socket.on('connect', function() {
            console.log('Socket.IOに接続しました');
            hideConnectingMessage();
            showToast('チャットサーバーに接続しました', 'success');
        });

        socket.on('disconnect', function() {
            console.log('Socket.IOから切断されました');
            showConnectingMessage();
            showToast('チャットサーバーから切断されました', 'warning');
        });

        // メッセージイベント
        socket.on('room_message', function(data) {
            displayMessage(data);
        });

        // ユーザー管理イベント
        socket.on('user_joined', function(data) {
            displaySystemMessage(`${data.username}さんが参加しました`);
            updateMemberCount(data.memberCount);
            updateMemberList(data.members);
        });

        socket.on('user_left', function(data) {
            displaySystemMessage(`${data.username}さんが退出しました`);
            updateMemberCount(data.memberCount);
            updateMemberList(data.members);
        });

        // 入力状態イベント
        socket.on('user_typing', function(data) {
            showTypingIndicator(data.username);
        });

        socket.on('user_stop_typing', function(data) {
            hideTypingIndicator(data.username);
        });

        // エラーイベント
        socket.on('error', function(error) {
            console.error('Socket.IOエラー:', error);
            showToast('通信エラーが発生しました', 'danger');
        });

    } catch (error) {
        console.error('Socket.IO初期化エラー:', error);
        hideConnectingMessage();
        showToast('チャットサーバーとの接続に失敗しました（表示のみモード）', 'warning');
    }
}

/**
 * メッセージ入力の設定
 */
function setupMessageInput() {
    const messageInput = document.getElementById('messageInput');
    const messageForm = document.getElementById('messageForm');
    const sendButton = document.getElementById('sendButton');
    const messageLength = document.getElementById('messageLength');

    if (!messageInput || !messageForm) {
        console.error('メッセージ入力要素が見つかりません');
        return;
    }

    // 文字数カウントと送信ボタン制御
    messageInput.addEventListener('input', function() {
        const length = this.value.length;
        if (messageLength) {
            messageLength.textContent = length;
        }

        // 送信ボタンの有効/無効制御
        if (sendButton) {
            sendButton.disabled = length === 0 || length > 500;
        }

        // 自動リサイズ
        autoResizeTextarea(this);

        // 入力状態の通知
        handleTypingIndicator();
    });

    // Enterキーでの送信（Shift+Enterは改行）
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // フォーム送信
    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });
}

/**
 * UIイベントの設定
 */
function setupUIEvents() {
    // 絵文字ボタン
    const emojiButton = document.getElementById('emojiButton');
    const emojiContainer = document.getElementById('emojiPickerContainer');

    if (emojiButton && emojiContainer) {
        emojiButton.addEventListener('click', function() {
            const isVisible = emojiContainer.style.display !== 'none';
            emojiContainer.style.display = isVisible ? 'none' : 'block';
        });

        // 外側クリックで閉じる
        document.addEventListener('click', function(e) {
            if (!emojiButton.contains(e.target) && !emojiContainer.contains(e.target)) {
                emojiContainer.style.display = 'none';
            }
        });
    }

    // ルーム退出ボタン
    const confirmLeaveBtn = document.getElementById('confirmLeaveRoom');
    if (confirmLeaveBtn) {
        confirmLeaveBtn.addEventListener('click', leaveRoom);
    }

    // ルーム設定保存（オーナーのみ）
    const saveSettingsBtn = document.getElementById('saveRoomSettings');
    if (saveSettingsBtn) {
        saveSettingsBtn.addEventListener('click', saveRoomSettings);
    }
}

/**
 * ルームに参加
 */
function joinRoom() {
    if (!currentRoom || !currentUser) {
        console.error('ルーム、またはユーザー情報が不足しています');
        return;
    }

    if (!socket) {
        console.warn('Socket.IOが利用できません。基本表示のみ有効です。');
        hideConnectingMessage();
        showToast(`${currentRoom.name} に参加しました（表示のみモード）`, 'info');
        loadStaticMessages(); // 静的なメッセージを読み込む（実装可能であれば）
        return;
    }

    socket.emit('join_room', {
        room_id: currentRoom.id,
        username: currentUser.name,
        user_id: currentUser.id
    });
}

/**
 * 静的なメッセージを読み込む（SocketIO無効時用）
 */
function loadStaticMessages() {
    // 実装予定: REST APIで過去のメッセージを取得
    console.log('静的メッセージの読み込み機能は未実装です');
}

    // キーボードショートカット
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            if (e.shiftKey) {
                // Shift+Enter: 改行（デフォルト動作）
                return;
            } else {
                // Enter: 送信
                e.preventDefault();
                sendMessage();
            }
        }
    });

    // フォーム送信
    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });
}

/**
 * UIイベントの設定
 */
function setupUIEvents() {
    // 退出ボタンのイベント設定は個別の関数で行う
}

/**
 * メッセージ送信
 */
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    if (!messageInput || !socket) return;

    const messageText = messageInput.value.trim();
    if (messageText === '' || messageText.length > 500) return;

    // メッセージを送信
    socket.emit('send_message', {
        room_id: currentRoom.id,
        message: messageText,
        username: currentUser.name,
        user_id: currentUser.id
    });

    // 入力フィールドをクリア
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // 送信ボタンを無効化
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.disabled = true;
    }

    // 文字数表示をリセット
    const messageLength = document.getElementById('messageLength');
    if (messageLength) {
        messageLength.textContent = '0';
    }

    // 入力状態を解除
    stopTyping();
}

/**
 * メッセージを表示
 */
function displayMessage(data) {
    const messagesList = document.getElementById('messagesList');
    if (!messagesList) return;

    // ウェルカムメッセージを非表示
    const welcomeMessage = document.getElementById('welcomeMessage');
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }

    const messageDiv = document.createElement('div');
    const isOwn = data.user_id === currentUser.id;

    messageDiv.className = `message-bubble ${isOwn ? 'own' : 'other'}`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    // メッセージ作成者（自分以外の場合のみ表示）
    if (!isOwn) {
        const messageAuthor = document.createElement('div');
        messageAuthor.className = 'message-author';
        messageAuthor.textContent = data.username;
        messageContent.appendChild(messageAuthor);
    }

    // メッセージテキスト
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = data.message;
    messageContent.appendChild(messageText);

    // タイムスタンプ
    const messageInfo = document.createElement('div');
    messageInfo.className = 'message-info';
    messageInfo.textContent = formatTime(data.timestamp);
    messageContent.appendChild(messageInfo);

    messageDiv.appendChild(messageContent);
    messagesList.appendChild(messageDiv);

    // スクロールを最下部に
    scrollToBottom();
}

/**
 * システムメッセージを表示
 */
function displaySystemMessage(message) {
    const messagesList = document.getElementById('messagesList');
    if (!messagesList) return;

    const systemDiv = document.createElement('div');
    systemDiv.className = 'system-message';
    systemDiv.innerHTML = `<i class="bi bi-info-circle me-1"></i>${message}`;

    messagesList.appendChild(systemDiv);
    scrollToBottom();
}

/**
 * 絵文字を挿入
 */
function insertEmoji(emoji) {
    const messageInput = document.getElementById('messageInput');
    if (!messageInput) return;

    const cursorPos = messageInput.selectionStart;
    const textBefore = messageInput.value.substring(0, cursorPos);
    const textAfter = messageInput.value.substring(messageInput.selectionEnd);

    messageInput.value = textBefore + emoji + textAfter;
    messageInput.selectionStart = messageInput.selectionEnd = cursorPos + emoji.length;

    // フォーカスを戻す
    messageInput.focus();

    // 入力イベントをトリガー
    messageInput.dispatchEvent(new Event('input'));

    // 絵文字ピッカーを閉じる
    const emojiContainer = document.getElementById('emojiPickerContainer');
    if (emojiContainer) {
        emojiContainer.style.display = 'none';
    }
}

/**
 * テキストエリアの自動リサイズ
 */
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

/**
 * 入力状態の処理
 */
function handleTypingIndicator() {
    if (!isTyping) {
        isTyping = true;
        if (socket) {
            socket.emit('start_typing', {
                room_id: currentRoom.id,
                username: currentUser.name
            });
        }
    }

    // タイマーをリセット
    clearTimeout(typingTimer);
    typingTimer = setTimeout(stopTyping, 2000);
}

/**
 * 入力状態を停止
 */
function stopTyping() {
    if (isTyping) {
        isTyping = false;
        if (socket) {
            socket.emit('stop_typing', {
                room_id: currentRoom.id,
                username: currentUser.name
            });
        }
    }
    clearTimeout(typingTimer);
}

/**
 * 入力状態表示
 */
function showTypingIndicator(username) {
    const indicator = document.getElementById('typingIndicator');
    const usersSpan = document.getElementById('typingUsers');

    if (!indicator || !usersSpan) return;

    usersSpan.textContent = username;
    indicator.style.display = 'block';
}

/**
 * 入力状態非表示
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

/**
 * メンバー数更新
 */
function updateMemberCount(count) {
    const memberCount = document.getElementById('memberCount');
    const memberCountSidebar = document.getElementById('memberCountSidebar');

    if (memberCount) {
        memberCount.textContent = count;
    }
    if (memberCountSidebar) {
        memberCountSidebar.textContent = count;
    }
}

/**
 * メンバーリスト更新
 */
function updateMemberList(members) {
    const memberList = document.getElementById('memberList');
    if (!memberList || !Array.isArray(members)) return;

    memberList.innerHTML = '';

    members.forEach(member => {
        const memberDiv = document.createElement('div');
        memberDiv.className = 'member-item';

        // アバター
        const avatar = document.createElement('div');
        avatar.className = 'member-avatar';
        avatar.textContent = member.name.charAt(0).toUpperCase();

        // メンバー情報
        const memberInfo = document.createElement('div');
        memberInfo.className = 'member-info';

        const memberName = document.createElement('div');
        memberName.className = 'member-name';
        memberName.textContent = member.name;

        const memberRole = document.createElement('div');
        memberRole.className = 'member-role';
        memberRole.textContent = member.isOwner ? 'オーナー' : (member.isAdmin ? '管理者' : 'メンバー');

        // オンライン状態
        const status = document.createElement('div');
        status.className = `member-status ${member.online ? 'online' : 'offline'}`;

        memberInfo.appendChild(memberName);
        memberInfo.appendChild(memberRole);

        memberDiv.appendChild(avatar);
        memberDiv.appendChild(memberInfo);
        memberDiv.appendChild(status);

        memberList.appendChild(memberDiv);
    });
}

/**
 * ルームを退出
 */
function leaveRoom() {
    if (socket) {
        socket.emit('leave_room', {
            room_id: currentRoom.id,
            username: currentUser.name
        });
    }

    // ルーム一覧に戻る
    window.location.href = '/room/';
}

/**
 * チャット履歴をクリア
 */
function clearChat() {
    const messagesList = document.getElementById('messagesList');
    if (messagesList) {
        messagesList.innerHTML = '';

        // ウェルカムメッセージを再表示
        const welcomeMessage = document.getElementById('welcomeMessage');
        if (welcomeMessage) {
            welcomeMessage.style.display = 'block';
        }
    }

    showToast('チャット履歴をクリアしました', 'info');
}

/**
 * ルーム設定を保存
 */
function saveRoomSettings() {
    if (!currentUser.isOwner && !currentUser.isAdmin) {
        showToast('設定を変更する権限がありません', 'danger');
        return;
    }

    const roomName = document.getElementById('roomNameSetting')?.value;
    const roomDescription = document.getElementById('roomDescriptionSetting')?.value;
    const maxMembers = document.getElementById('maxMembersSetting')?.value;
    const roomPassword = document.getElementById('roomPasswordSetting')?.value;

    if (!roomName?.trim()) {
        showToast('ルーム名を入力してください', 'danger');
        return;
    }

    const settings = {
        room_id: currentRoom.id,
        name: roomName.trim(),
        description: roomDescription?.trim() || '',
        max_members: parseInt(maxMembers) || 50,
        password: roomPassword?.trim() || null
    };

    if (socket) {
        socket.emit('update_room_settings', settings);
    }

    // モーダルを閉じる
    const modal = bootstrap.Modal.getInstance(document.getElementById('roomSettingsModal'));
    if (modal) {
        modal.hide();
    }

    showToast('設定を保存しました', 'success');
}

/**
 * 接続中メッセージを表示
 */
function showConnectingMessage() {
    const connectingMessage = document.getElementById('connectingMessage');
    if (connectingMessage) {
        connectingMessage.style.display = 'block';
    }
}

/**
 * 接続中メッセージを非表示
 */
function hideConnectingMessage() {
    const connectingMessage = document.getElementById('connectingMessage');
    if (connectingMessage) {
        connectingMessage.style.display = 'none';
    }
}

/**
 * 最下部までスクロール
 */
function scrollToBottom() {
    const container = document.getElementById('messagesContainer');
    if (container) {
        setTimeout(() => {
            container.scrollTop = container.scrollHeight;
        }, 100);
    }
}

/**
 * 時刻フォーマット
 */
function formatTime(timestamp) {
    if (!timestamp) return '';

    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMinutes = Math.floor(diffMs / 60000);

    if (diffMinutes < 1) {
        return 'たった今';
    } else if (diffMinutes < 60) {
        return `${diffMinutes}分前`;
    } else if (diffMinutes < 1440) { // 24時間
        const diffHours = Math.floor(diffMinutes / 60);
        return `${diffHours}時間前`;
    } else {
        return date.toLocaleDateString('ja-JP', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

/**
 * トースト通知を表示
 */
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) return;

    const toastEl = document.getElementById('notificationToast');
    const toastBody = document.getElementById('toastMessage');

    if (!toastEl || !toastBody) return;

    // トーストのスタイルを設定
    toastEl.className = `toast align-items-center border-0 bg-${type}`;
    toastBody.textContent = message;

    // トーストを表示
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

// ページ離脱時にSocket.IOを切断
window.addEventListener('beforeunload', function() {
    if (socket) {
        socket.disconnect();
    }
});
