/**
 * SweetAlert2を使用したアラート・確認ダイアログ共通関数
 */

/**
 * SweetAlert2の標準アイコン用CSS設定（必要に応じて軽微な調整のみ）
 */
function addStandardIconStyles() {
    // 特別なスタイル調整が必要な場合のみ追加
    if (!document.querySelector('#swal-standard-icon-style')) {
        const style = document.createElement('style');
        style.textContent = `
            /* 必要に応じて軽微な調整を追加 */
        `;
        style.id = 'swal-standard-icon-style';
        document.head.appendChild(style);
    }
}

/**
 * 情報アラートを表示
 * @param {string} title - タイトル
 * @param {string} text - メッセージ本文
 * @param {string} icon - アイコン（success, error, warning, info, question）
 */
function showSwalAlert(title, text = '', icon = 'info') {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: title,
            text: text,
            icon: icon,
            confirmButtonText: 'OK',
            confirmButtonColor: '#3085d6'
        });
    } else {
        // フォールバック：通常のalert
        alert(`${title}\n${text}`);
    }
}

/**
 * 成功メッセージを表示
 * @param {string} title - タイトル
 * @param {string} text - メッセージ本文
 */
function showSuccessAlert(title, text = '') {
    showSwalAlert(title, text, 'success');
}

/**
 * エラーメッセージを表示
 * @param {string} title - タイトル
 * @param {string} text - メッセージ本文
 */
function showErrorAlert(title, text = '') {
    showSwalAlert(title, text, 'error');
}

/**
 * 警告メッセージを表示
 * @param {string} title - タイトル
 * @param {string} text - メッセージ本文
 */
function showWarningAlert(title, text = '') {
    showSwalAlert(title, text, 'warning');
}

/**
 * 確認ダイアログを表示
 * @param {string} title - タイトル
 * @param {string} text - メッセージ本文
 * @param {Function} onConfirm - OKボタン押下時のコールバック
 * @param {Function} onCancel - キャンセルボタン押下時のコールバック（オプション）
 */
function showConfirmDialog(title, text = '', onConfirm = null, onCancel = null) {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: title,
            text: text,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'はい',
            cancelButtonText: 'キャンセル',
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33'
        }).then((result) => {
            if (result.isConfirmed && onConfirm) {
                onConfirm();
            } else if (result.isDismissed && onCancel) {
                onCancel();
            }
        });
    } else {
        // フォールバック：通常のconfirm
        if (confirm(`${title}\n${text}`) && onConfirm) {
            onConfirm();
        }
    }
}

/**
 * 既存のalert()関数をSweetAlert2で置き換え（拡張版）
 * @param {string} title - タイトル（省略時は'通知'）
 * @param {string} message - メッセージ（省略時は''）
 * @param {string} icon - アイコン（省略時は'info'）
 * @param {function} callback - コールバック関数（省略可能）
 */
function swal_alert(title = '通知', message = '', icon = 'info', callback = null) {
    // 引数が1つだけの場合（後方互換性）
    if (arguments.length === 1 && typeof title === 'string') {
        message = title;
        title = '通知';
        icon = 'info';
    }

    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: title,
            text: message,
            icon: icon,
            confirmButtonText: 'OK',
            confirmButtonColor: '#3085d6'
        }).then((result) => {
            if (callback && typeof callback === 'function') {
                callback(result);
            }
        });
    } else {
        // フォールバック：通常のalert
        alert(`${title}\n${message}`);
        if (callback && typeof callback === 'function') {
            callback(true);
        }
    }
}

/**
 * 既存のconfirm()関数をSweetAlert2で置き換え
 * @param {string} message - メッセージ
 * @returns {Promise} - 確認結果のPromise
 */
function swal_confirm(message) {
    if (typeof Swal !== 'undefined') {
        return Swal.fire({
            title: '確認',
            text: message,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'はい',
            cancelButtonText: 'キャンセル',
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33'
        }).then((result) => {
            return result.isConfirmed;
        });
    } else {
        // フォールバック：通常のconfirm
        return Promise.resolve(confirm(message));
    }
}
