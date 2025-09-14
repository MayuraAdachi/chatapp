// 統計ページのJavaScript機能
class StatisticsManager {
    constructor() {
        this.initCharts();
        this.setupAutoRefresh();
    }

    // チャートの初期化（データは外部から提供される）
    initCharts() {
        // ユーザー構成グラフ
        if (document.getElementById('userChart')) {
            this.createUserChart();
        }

        // ルーム構成グラフ
        if (document.getElementById('roomChart')) {
            this.roomCreateChart();
        }
    }

    // ユーザーグラフ作成（データは外部から設定される）
    createUserChart() {
        const userCtx = document.getElementById('userChart').getContext('2d');

        // データはwindow.statsDataから取得
        if (!window.statsData || !window.statsData.userStats) {
            return;
        }

        const userStats = window.statsData.userStats;
        new Chart(userCtx, {
            type: 'doughnut',
            data: {
                labels: ['オンライン', 'オフライン', '管理者'],
                datasets: [{
                    data: [
                        userStats.online,
                        userStats.total - userStats.online,
                        userStats.admins
                    ],
                    backgroundColor: ['#28a745', '#6c757d', '#ffc107']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // ルームグラフ作成（データは外部から設定される）
    roomCreateChart() {
        const roomCtx = document.getElementById('roomChart').getContext('2d');

        // データはwindow.statsDataから取得
        if (!window.statsData || !window.statsData.roomStats) {
            return;
        }

        const roomStats = window.statsData.roomStats;
        new Chart(roomCtx, {
            type: 'pie',
            data: {
                labels: ['パブリック', 'プライベート'],
                datasets: [{
                    data: [roomStats.public, roomStats.private],
                    backgroundColor: ['#007bff', '#dc3545']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // 統計の更新
    refreshStats() {
        if (!window.statsData || !window.statsData.apiUrl) {
            return;
        }

        fetch(window.statsData.apiUrl)
            .then(response => response.json())
            .then(data => {
                location.reload(); // 簡単な実装として画面をリロード
            })        .catch(error => {
            console.error('統計更新エラー:', error);
            showErrorAlert('エラー', '統計の更新に失敗しました');
        });
    }

    // 自動更新の設定
    setupAutoRefresh() {
        // 5分ごとに自動更新
        setInterval(() => this.refreshStats(), 5 * 60 * 1000);
    }
}

// ページロード時に初期化
document.addEventListener('DOMContentLoaded', function() {
    window.statisticsManager = new StatisticsManager();
});

// グローバル関数として公開（HTMLから呼び出し可能）
function refreshStats() {
    if (window.statisticsManager) {
        window.statisticsManager.refreshStats();
    }
}
