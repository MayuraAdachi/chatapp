// チャット画面用JavaScript - 簡易版（SocketIO無効時対応）

let socket;
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
        });

        socket.on('user_left', function(data) {
            displaySystemMessage(`${data.username}さんが退出しました`);
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

    if (!messageInput || !messageForm) {
        console.error('メッセージ入力要素が見つかりません');
        return;
    }

    // 文字数カウントと送信ボタン制御
    messageInput.addEventListener('input', function() {
        const length = this.value.length;

        // 送信ボタンの有効/無効制御
        if (sendButton) {
            sendButton.disabled = length === 0 || length > 500;
        }

        // 自動リサイズ
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
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
    // 基本的なUI設定
    const confirmLeaveBtn = document.getElementById('confirmLeaveRoom');
    if (confirmLeaveBtn) {
        confirmLeaveBtn.addEventListener('click', function() {
            window.location.href = '/room/';
        });
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
        return;
    }

    socket.emit('join_room', {
        room_id: currentRoom.id,
        username: currentUser.name,
        user_id: currentUser.id
    });
}

/**
 * メッセージを送信
 */
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();

    if (!message) return;

    if (!socket) {
        showToast('リアルタイム機能が無効のため、メッセージを送信できません', 'warning');
        return;
    }

    socket.emit('send_message', {
        room_id: currentRoom.id,
        message: message,
        username: currentUser.name,
        user_id: currentUser.id
    });

    messageInput.value = '';
    messageInput.style.height = 'auto';
}

/**
 * 接続中メッセージを表示
 */
function showConnectingMessage() {
    const connectingDiv = document.getElementById('connectingMessage');
    if (connectingDiv) {
        connectingDiv.style.display = 'block';
    }
}

/**
 * 接続中メッセージを非表示
 */
function hideConnectingMessage() {
    const connectingDiv = document.getElementById('connectingMessage');
    if (connectingDiv) {
        connectingDiv.style.display = 'none';
    }
}

/**
 * トースト通知を表示
 */
function showToast(message, type = 'info') {
    // 簡易的なアラート表示（将来的にはToast UIに変更）
    const alertClass = {
        'success': 'alert-success',
        'warning': 'alert-warning',
        'danger': 'alert-danger',
        'info': 'alert-info'
    }[type] || 'alert-info';

    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const alertContainer = document.getElementById('alertContainer') || document.body;
    alertContainer.insertAdjacentHTML('afterbegin', alertHtml);

    // 3秒後に自動削除
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        if (alerts.length > 0) {
            alerts[0].remove();
        }
    }, 3000);
}

/**
 * システムメッセージを表示
 */
function displaySystemMessage(message) {
    console.log('システムメッセージ:', message);
    // 実装予定: チャット画面にシステムメッセージを表示
}

/**
 * メッセージを表示
 */
function displayMessage(data) {
    console.log('メッセージ:', data);
    // 実装予定: チャット画面にメッセージを表示
}
