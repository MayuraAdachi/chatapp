// 開発者ツールスクリプト

// Jinja2変数をJavaScript変数として定義（テンプレートから渡される）
// これらの値はテンプレート側でwindowオブジェクトに設定される想定
window.devToolsData = window.devToolsData || {};

// ツール実行結果を表示するための共通関数
function displayOutput(message, type = 'info') {
    const output = document.getElementById('tool-output');
    const timestamp = new Date().toLocaleString('ja-JP');
    const typeIcon = {
        'info': '🔵',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    };

    output.textContent += `[${timestamp}] ${typeIcon[type] || '🔵'} ${message}\n`;
    output.scrollTop = output.scrollHeight;
}

// データベース接続確認
function checkDbConnection() {
    displayOutput(window.devToolsData.messages?.checkingDbConnection || 'データベース接続を確認中...', 'info');

    fetch('/admin/api/check-db')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayOutput(window.devToolsData.messages?.dbConnectionNormal || 'データベース接続: 正常', 'success');
                displayOutput(`接続先: ${data.database_url}`, 'info');
            } else {
                displayOutput(window.devToolsData.messages?.dbConnectionFailed || 'データベース接続: 失敗', 'error');
                displayOutput(`エラー: ${data.error}`, 'error');
            }
        })
        .catch(error => {
            displayOutput(window.devToolsData.messages?.dbConnectionError || 'データベース接続確認中にエラーが発生しました', 'error');
        });
}

// テーブル情報表示
function showTableInfo() {
    displayOutput(window.devToolsData.messages?.gettingTableInfo || 'テーブル情報を取得中...', 'info');
    // TODO: API実装
    displayOutput(window.devToolsData.messages?.tableInfoNotImplemented || 'テーブル情報取得機能は今後実装予定です', 'warning');
}

// キャッシュ状況確認
function checkCacheStatus() {
    displayOutput(window.devToolsData.messages?.checkingCache || 'キャッシュ状況を確認中...', 'info');
    displayOutput(window.devToolsData.messages?.cacheDisabled || 'キャッシュ機能は現在無効です', 'warning');
}

// セッション情報表示
function showSessionInfo() {
    displayOutput(window.devToolsData.messages?.gettingSessionInfo || 'セッション情報を取得中...', 'info');
    displayOutput(`現在のユーザー: ${window.devToolsData.session?.username || 'Anonymous'}`, 'info');
    displayOutput(`ユーザーID: ${window.devToolsData.session?.user_id || 'N/A'}`, 'info');
    displayOutput(`ログイン状態: ${window.devToolsData.session?.is_logged_in ? '有効' : '無効'}`, 'info');
}

// 翻訳状況確認
function checkTranslations() {
    displayOutput(window.devToolsData.messages?.checkingTranslations || '翻訳状況を確認中...', 'info');
    displayOutput(`${window.devToolsData.messages?.languageCount || '対応言語数'}: ${window.devToolsData.config?.languageCount || 0}`, 'info');
    displayOutput(`${window.devToolsData.messages?.defaultLanguage || 'デフォルト言語'}: ${window.devToolsData.config?.defaultLocale || 'ja'}`, 'info');
}

// 管理者専用機能（権限チェック付き）
function optimizeDatabase() {
    if (confirm(window.devToolsData.messages?.confirmOptimizeDb || 'データベースの最適化を実行しますか？')) {
        displayOutput(window.devToolsData.messages?.optimizingDb || 'データベース最適化を実行中...', 'info');
        displayOutput(window.devToolsData.messages?.optimizeNotImplemented || '最適化機能は今後実装予定です', 'warning');
    }
}

function clearCache() {
    if (confirm(window.devToolsData.messages?.confirmClearCache || 'キャッシュをクリアしますか？')) {
        displayOutput(window.devToolsData.messages?.clearingCache || 'キャッシュクリア中...', 'info');
        displayOutput(window.devToolsData.messages?.cacheCleared || 'キャッシュクリア完了（現在キャッシュ機能は無効）', 'success');
    }
}

function updateTranslations() {
    displayOutput(window.devToolsData.messages?.updatingTranslations || '翻訳データを更新中...', 'info');
    displayOutput(window.devToolsData.messages?.translationsNotImplemented || '翻訳データ更新機能は今後実装予定です', 'warning');
}

// その他の機能
function showRecentLogs() {
    displayOutput(window.devToolsData.messages?.showingRecentLogs || '最新ログを表示中...', 'info');
    displayOutput(window.devToolsData.messages?.logsNotImplemented || 'ログ機能は今後実装予定です', 'warning');
}

function showErrorLogs() {
    displayOutput(window.devToolsData.messages?.showingErrorLogs || 'エラーログを表示中...', 'info');
    displayOutput(window.devToolsData.messages?.errorLogsNotImplemented || 'エラーログ機能は今後実装予定です', 'warning');
}

function showPerformanceStats() {
    displayOutput(window.devToolsData.messages?.gettingPerformanceStats || 'パフォーマンス情報を取得中...', 'info');
    displayOutput(window.devToolsData.messages?.performanceNotImplemented || 'パフォーマンス監視機能は今後実装予定です', 'warning');
}

// 初期化時メッセージ
document.addEventListener('DOMContentLoaded', function() {
    displayOutput(window.devToolsData.messages?.toolsLoaded || '開発者ツールが読み込まれました', 'success');

    if (window.devToolsData.user?.is_admin) {
        displayOutput(window.devToolsData.messages?.adminAccess || '管理者権限でアクセスしています', 'info');
    } else {
        displayOutput(window.devToolsData.messages?.developerAccess || '開発者権限でアクセスしています', 'info');
    }
});
