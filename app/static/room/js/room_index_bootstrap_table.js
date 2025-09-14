// ルーム一覧ページのBootstrap Table機能

// ページ読み込み完了時の初期化処理
document.addEventListener('DOMContentLoaded', function () {
    // jQueryとBootstrap Tableの存在確認
    if (typeof $ === 'undefined') {
        return;
    }

    if (typeof $.fn.bootstrapTable === 'undefined') {
        return;
    }

    // Bootstrap Tableの初期化
    const $table = $('#roomTable');

    if ($table.length > 0) {
        // 既に初期化されているかチェック
        if ($table.data('bootstrap.table')) {
            $table.bootstrapTable('destroy');
        }

        // Bootstrap Tableの初期化オプション
        $table.bootstrapTable({
            locale: 'ja-JP',
            search: false,
            searchHighlight: true,
            showRefresh: false,
            showToggle: false,
            showColumns: false,
            sortName: 'created_at',
            sortOrder: 'desc',
            sortable: true,
            sortStable: true,
            pagination: true,
            pageSize: 10,
            pageList: [10, 20, 30, 40, 50, 'All'],
            showPaginationSwitch: false,
            showInfoBar: false,
            showSearchClearButton: false,
            searchTimeOut: 500,
            trimOnSearch: true,
            clickToSelect: false,
            maintainSelected: false,
            sidePagination: 'client',
            formatNoMatches: function () {
                return '<div class="text-center py-4">' +
                    '<i class="fas fa-search fa-3x text-muted mb-3"></i>' +
                    '<h5 class="text-muted">検索結果が見つかりません</h5>' +
                    '<p class="text-muted">検索条件を変更してお試しください</p>' +
                    '</div>';
            },
            formatAllRows: function () {
                return '全て';
            }
        });

        // ソートのカスタマイズ
        $table.on('sort.bs.table', function (e, name, order) {
        });

        // カスタムイベントハンドラー
        $table.on('refresh.bs.table', function () {
        });

        $table.on('search.bs.table', function () {
            updateRoomCount();
        });

        $table.on('page-change.bs.table', function (e, number, size) {
        });

        // 初期化後の処理
        setTimeout(() => {
            updateRoomCount();
            setupQuickSearch();
            addPaginationInfo();
        }, 100);
    }

    // フラッシュメッセージの処理
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function (message) {
        const messageText = message.textContent.trim();
        const isSuccess = message.classList.contains('alert-success');
        const isError = message.classList.contains('alert-danger') || message.classList.contains('alert-error');

        if (messageText && (isSuccess || isError)) {
            message.style.display = 'none';
            if (typeof swal_alert === 'function') {
                if (isSuccess) {
                    swal_alert('成功', messageText, 'success', function () {
                        // 成功時はテーブルを更新
                        if ($table.length > 0) {
                            $table.bootstrapTable('refresh');
                        }
                    });
                } else if (isError) {
                    swal_alert('エラー', messageText, 'error');
                }
            } else {
                alert(messageText);
            }
        }
    });
});

/**
 * 表示件数を更新
 */
function updateRoomCount() {
    const $table = $('#roomTable');
    if ($table.length > 0) {
        const data = $table.bootstrapTable('getData');
        const filteredData = $table.bootstrapTable('getData', { useCurrentPage: false, includeHiddenRows: false });

        const countElement = document.querySelector('.room-count');
        if (countElement) {
            if (data.length === filteredData.length) {
                countElement.textContent = `${data.length} 件`;
            } else {
                countElement.textContent = `${filteredData.length} / ${data.length} 件`;
            }
        }
    }
}

/**
 * クイック検索機能の設定
 */
function setupQuickSearch() {
    const quickSearchInput = document.getElementById('quickSearchInput');
    const clearQuickSearch = document.getElementById('clearQuickSearch');
    const $table = $('#roomTable');

    if (quickSearchInput && $table.length > 0) {
        // リアルタイム検索
        let searchTimeout;
        quickSearchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const searchTerm = this.value.trim();

            searchTimeout = setTimeout(() => {
                // Bootstrap Tableの検索機能を使用
                $table.bootstrapTable('resetSearch', searchTerm);
                updateRoomCount();
            }, 300);
        });

        // Enterキーでの検索
        quickSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const searchTerm = this.value.trim();
                $table.bootstrapTable('resetSearch', searchTerm);
                updateRoomCount();
            }
        });

        // 検索クリアボタン
        if (clearQuickSearch) {
            clearQuickSearch.addEventListener('click', function() {
                quickSearchInput.value = '';
                $table.bootstrapTable('resetSearch', '');
                updateRoomCount();
                quickSearchInput.focus();
            });
        }

        // 検索ボックスのプレースホルダー更新機能

        quickSearchInput.addEventListener('blur', function() {
            this.placeholder = 'ルーム名や説明で検索...';
        });
    }
}

/**
 * テーブルを手動で更新
 */
function refreshRoomTable() {
    const $table = $('#roomTable');
    if ($table.length > 0) {
        $table.bootstrapTable('refresh');
        updateRoomCount();
    }
}

/**
 * ページネーション情報と標準ページャーを上下に表示
 */
function addPaginationInfo() {
    const $table = $('#roomTable');
    if ($table.length === 0) return;

    // 既存の要素をクリア
    $('#pagination-info-top, #pagination-info-bottom, #pagination-top').remove();

    // 情報表示用のコンテナを追加（テーブルの直前・直後に）
    $table.before('<div id="pagination-info-top" class="text-end text-muted small mb-2"></div>');
    $table.after('<div id="pagination-info-bottom" class="text-end text-muted small mt-2"></div>');

    // 情報を更新する関数
    function updateInfo() {
        const options = $table.bootstrapTable('getOptions');
        const totalRows = $table.bootstrapTable('getData').length;
        const pageNumber = options.pageNumber || 1;
        const pageSize = options.pageSize || 6;

        let infoText = '0 件の結果';
        if (totalRows > 0) {
            const startRow = (pageNumber - 1) * pageSize + 1;
            const endRow = Math.min(pageNumber * pageSize, totalRows);
            infoText = `${totalRows} 件中 ${startRow} - ${endRow} 件を表示`;
        }

        $('#pagination-info-top, #pagination-info-bottom').text(infoText);
    }

    // イベント設定
    $table.on('page-change.bs.table search.bs.table load-success.bs.table refresh.bs.table', updateInfo);

    // Bootstrap 5のユーティリティクラスをページネーションに適用
    $table.on('post-body.bs.table', function() {
        setTimeout(() => {
            // ページネーション要素にBootstrap 5クラスを追加
            $('.fixed-table-pagination .pagination').addClass('justify-content-center');
            $('.fixed-table-pagination .page-link').addClass('fw-medium');
            $('.fixed-table-pagination .page-item.active .page-link').addClass('fw-semibold shadow-sm text-white');
        }, 50);
    });

    // 初回更新
    setTimeout(() => {
        updateInfo();
        // 初期化時にもBootstrap 5クラスを適用
        $('.fixed-table-pagination .pagination').addClass('justify-content-center');
        $('.fixed-table-pagination .page-link').addClass('fw-medium');
        $('.fixed-table-pagination .page-item.active .page-link').addClass('fw-semibold shadow-sm text-white');
    }, 150);
}
