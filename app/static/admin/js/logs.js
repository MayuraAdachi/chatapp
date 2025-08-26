// ログ管理スクリプト
let logUpdateInterval;

// ログの更新
function refreshLogs() {
    fetch(window.location.href)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newLogContainer = doc.getElementById('logContainer');
            if (newLogContainer) {
                document.getElementById('logContainer').innerHTML = newLogContainer.innerHTML;
                // 最下部までスクロール
                const container = document.getElementById('logContainer');
                container.scrollTop = container.scrollHeight;
            }
        })
        .catch(error => {
            console.error('ログ更新エラー:', error);
        });
}

// ログの擬似クリア（表示をクリアするだけ）
function clearLogs() {
    if (confirm('表示中のログをクリアしますか？（実際のログファイルは削除されません）')) {
        document.getElementById('logContainer').innerHTML =
            '<div class="log-line text-muted">ログをクリアしました。</div>';
    }
}

// リアルタイム統計の更新（仮実装）
function updateRealtimeStats() {
    // 実際の実装では、バックエンドAPIからデータを取得
    document.getElementById('cpuUsage').textContent = Math.floor(Math.random() * 30 + 10) + '%';
    document.getElementById('memoryUsage').textContent = Math.floor(Math.random() * 200 + 100) + 'MB';
    document.getElementById('activeConnections').textContent = Math.floor(Math.random() * 50 + 10);
    document.getElementById('uptime').textContent = Math.floor(Math.random() * 24) + 'h ' + Math.floor(Math.random() * 60) + 'm';
}

// 自動更新の開始
function startAutoUpdate() {
    // ログを10秒ごとに更新
    logUpdateInterval = setInterval(refreshLogs, 10000);

    // 統計を5秒ごとに更新
    setInterval(updateRealtimeStats, 5000);

    // 初回実行
    updateRealtimeStats();
}

// 自動更新の停止
function stopAutoUpdate() {
    if (logUpdateInterval) {
        clearInterval(logUpdateInterval);
    }
}

// ページロード時に自動更新開始
document.addEventListener('DOMContentLoaded', function() {
    startAutoUpdate();

    // 初回ログスクロール
    const container = document.getElementById('logContainer');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
});

// ページ離脱時に自動更新停止
window.addEventListener('beforeunload', stopAutoUpdate);
