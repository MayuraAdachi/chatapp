// ルーム一覧ページのJavaScript機能（ルーム固有機能のみ）

/**
 * ルームに参加する確認ダイアログを表示し、参加処理を実行
 * @param {string} roomId - ルームID
 * @param {string} roomName - ルーム名
 */
function joinRoom(roomId, roomName) {
    // パスワードが必要かどうかをチェック
    const roomRow = document.querySelector(`tr[data-room-id="${roomId}"]`);
    const hasPassword = roomRow ? roomRow.dataset.hasPassword === 'true' : false;

    if (hasPassword) {
        // パスワードが必要な場合は入力を求める
        showPasswordDialog(roomId, roomName);
    } else {
        // 直接参加確認
        showConfirmDialog(
            'ルーム参加',
            `${roomName}に参加しますか？`,
            function() {
                // CSRFトークンを取得
                const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
                console.log('CSRFトークン:', csrfToken);
                console.log('参加リクエスト送信:', roomId);

                // AjaxでJSONリクエストを送信
                fetch('/room/join', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        room_id: roomId
                    })
                })
                .then(response => {
                    console.log('レスポンス受信:', response);
                    return response.json();
                })
                .then(data => {
                    console.log('レスポンスデータ:', data);
                    if (data.success) {
                        // 成功時はレスポンスのredirect_urlまたは部屋名ベースのURLに遷移
                        const redirectUrl = data.redirect_url || `/room/chat/${encodeURIComponent(roomName)}`;
                        console.log('参加成功、遷移:', redirectUrl);
                        window.location.href = redirectUrl;
                    } else {
                        console.log('参加失敗:', data.message);
                        showAlert('参加失敗', data.message, 'error');
                    }
                })
                .catch(error => {
                    console.error('参加エラー:', error);
                    showAlert('エラー', '参加処理中にエラーが発生しました', 'error');
                });
            }
        );
    }
}

/**
 * パスワード入力ダイアログを表示
 * @param {string} roomId - ルームID
 * @param {string} roomName - ルーム名
 */
function showPasswordDialog(roomId, roomName) {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: 'パスワードを入力',
            text: `ルーム「${roomName}」に参加するためのパスワードを入力してください`,
            input: 'password',
            inputAttributes: {
                autocapitalize: 'off',
                placeholder: 'パスワード'
            },
            showCancelButton: true,
            confirmButtonText: '参加',
            cancelButtonText: 'キャンセル',
            confirmButtonColor: '#28a745',
            cancelButtonColor: '#6c757d',
            preConfirm: (password) => {
                if (!password) {
                    Swal.showValidationMessage('パスワードを入力してください');
                }
                return password;
            }
        }).then((result) => {
            if (result.isConfirmed) {
                // CSRFトークンを取得
                const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

                // パスワード付きで参加リクエスト
                fetch('/room/join', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        room_id: roomId,
                        password: result.value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // 成功時はレスポンスのredirect_urlまたは部屋名ベースのURLに遷移
                        const redirectUrl = data.redirect_url || `/room/chat/${encodeURIComponent(roomName)}`;
                        window.location.href = redirectUrl;
                    } else {
                        showAlert('参加失敗', data.message, 'error');
                    }
                })
                .catch(error => {
                    console.error('参加エラー:', error);
                    showAlert('エラー', '参加処理中にエラーが発生しました', 'error');
                });
            }
        });
    } else {
        // SweetAlert2がない場合のフォールバック
        const password = prompt(`ルーム「${roomName}」のパスワードを入力してください:`);
        if (password !== null) {
            // CSRFトークンを取得
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

            fetch('/room/join', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    room_id: roomId,
                    password: password
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 成功時はレスポンスのredirect_urlまたは部屋名ベースのURLに遷移
                    const redirectUrl = data.redirect_url || `/room/chat/${encodeURIComponent(roomName)}`;
                    window.location.href = redirectUrl;
                } else {
                    alert('参加失敗: ' + data.message);
                }
            })
            .catch(error => {
                console.error('参加エラー:', error);
                alert('参加処理中にエラーが発生しました');
            });
        }
    }
}

/**
 * ルームを削除する確認ダイアログを表示し、削除処理を実行
 * @param {string} roomId - ルームID
 * @param {string} roomName - ルーム名
 */
function deleteRoom(roomId, roomName) {
    showConfirmDialog(
        'ルーム削除',
        `ルーム「${roomName}」を削除しますか？この操作は取り消せません。`,
        function() {
            // フォームを動的に作成して削除リクエストを送信
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/room/delete/${roomId}`;
            form.style.display = 'none';

            document.body.appendChild(form);
            form.submit();
        }
    );
}

/**
 * 確認ダイアログを表示（SweetAlert2使用）
 * @param {string} title - ダイアログタイトル
 * @param {string} message - メッセージ
 * @param {function} onConfirm - 確認時のコールバック
 */
function showConfirmDialog(title, message, onConfirm) {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: title,
            text: message,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'はい',
            cancelButtonText: 'キャンセル',
            confirmButtonColor: '#28a745',
            cancelButtonColor: '#6c757d',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                onConfirm();
            }
        });
    } else if (typeof swal_confirm === 'function') {
        swal_confirm(message).then((result) => {
            if (result) {
                onConfirm();
            }
        });
    } else {
        // フォールバック：通常のconfirm
        if (confirm(message)) {
            onConfirm();
        }
    }
}

/**
 * Bootstrap Tableを更新（room_index_bootstrap_table.jsの関数を呼び出し）
 */
function refreshBootstrapTable() {
    if (typeof refreshRoomTable === 'function') {
        refreshRoomTable();
    }
}

/**
 * ルーム作成・削除成功後にBootstrap Tableを更新
 */
function refreshRoomList() {
    refreshBootstrapTable();
}

/**
 * ルーム削除成功後の処理
 */
function onRoomDeleteSuccess(roomName) {
    if (typeof swal_alert === 'function') {
        swal_alert('削除完了', `ルーム「${roomName}」を削除しました。`, 'success', function() {
            refreshBootstrapTable();
        });
    }
}

// ページ読み込み完了時の初期化処理
document.addEventListener('DOMContentLoaded', function() {
    console.log('ルーム一覧ページが読み込まれました');

    // モーダルが閉じられた時の処理
    const createRoomModal = document.getElementById('createRoomModal');
    if (createRoomModal) {
        createRoomModal.addEventListener('hidden.bs.modal', function () {
            // フォームをリセット
            const form = this.querySelector('form');
            if (form) {
                form.reset();
                // デフォルト値を復元
                const maxMembersInput = form.querySelector('input[name="max_members"]');
                if (maxMembersInput && !maxMembersInput.value) {
                    maxMembersInput.value = '50';
                }
            }

            // エラー表示をクリア
            clearAllErrors();

            // 作成ボタンを有効化
            const createRoomBtn = document.getElementById('createRoomSubmit');
            if (createRoomBtn) {
                createRoomBtn.disabled = false;
            }
        });
    }

    // ルーム作成フォームのバリデーション（WTForms対応）
    const createRoomForm = document.getElementById('createRoomForm');
    const roomNameInput = document.querySelector('#createRoomForm input[name="room_name"]');
    const roomDescInput = document.querySelector('#createRoomForm textarea[name="room_description"]');
    const maxMembersInput = document.querySelector('#createRoomForm input[name="max_members"]');
    const roomPasswordInput = document.querySelector('#createRoomForm input[name="room_password"]');
    const createRoomBtn = document.getElementById('createRoomSubmit');

    if (roomNameInput && createRoomBtn) {
        // リアルタイムバリデーション
        roomNameInput.addEventListener('input', validateRoomForm);
        if (roomDescInput) roomDescInput.addEventListener('input', validateRoomForm);
        if (maxMembersInput) maxMembersInput.addEventListener('input', validateRoomForm);
        if (roomPasswordInput) roomPasswordInput.addEventListener('input', validateRoomForm);
    }

    /**
     * フォームバリデーション関数
     */
    function validateRoomForm() {
        // WTFormsを使ったサーバーサイドバリデーション
        if (createRoomForm) {
            const formData = new FormData(createRoomForm);

            fetch('/room/validate-form', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                clearAllErrors();

                if (data.success) {
                    // バリデーション成功
                    if (createRoomBtn) {
                        createRoomBtn.disabled = false;
                    }
                } else {
                    // バリデーションエラー
                    if (createRoomBtn) {
                        createRoomBtn.disabled = true;
                    }
                    displayErrors(data.errors);
                }
            })
            .catch(error => {
                console.error('バリデーションエラー:', error);
                if (typeof swal_alert === 'function') {
                    swal_alert('通信エラー', 'サーバーとの通信に失敗しました。フォームを再度確認してください。', 'error');
                }
                // フォールバック: クライアントサイドバリデーション
                performClientSideValidation();
            });
        } else {
            // フォールバック: クライアントサイドバリデーション
            performClientSideValidation();
        }
    }

    /**
     * クライアントサイドバリデーション
     */
    function performClientSideValidation() {
        let isValid = true;
        let errorMessage = '';

        // ルーム名バリデーション
        const roomName = roomNameInput.value.trim();
        if (!roomName) {
            isValid = false;
            errorMessage = 'ルーム名を入力してください';
        } else if (roomName.length > 100) {
            isValid = false;
            errorMessage = 'ルーム名は100文字以内で入力してください';
        }

        // 説明文バリデーション
        if (roomDescInput && roomDescInput.value.length > 500) {
            isValid = false;
            errorMessage = 'ルーム説明は500文字以内で入力してください';
        }

        // 最大メンバー数バリデーション
        if (maxMembersInput) {
            const maxMembers = parseInt(maxMembersInput.value);
            if (isNaN(maxMembers) || maxMembers < 2 || maxMembers > 100) {
                isValid = false;
                errorMessage = '最大メンバー数は2〜100の範囲で入力してください';
            }
        }

        // パスワードバリデーション（任意項目）
        if (roomPasswordInput && roomPasswordInput.value.trim()) {
            const password = roomPasswordInput.value.trim();
            if (password.length < 4 || password.length > 32) {
                isValid = false;
                errorMessage = 'パスワードは4〜32文字で入力してください';
            } else if (!/^[a-zA-Z0-9]+$/.test(password)) {
                isValid = false;
                errorMessage = 'パスワードは半角英数字のみ使用できます';
            }
        }

        // エラー表示の更新
        updateValidationUI(isValid, errorMessage);

        // 作成ボタンの状態更新
        if (createRoomBtn) {
            createRoomBtn.disabled = !isValid;
        }
    }

    /**
     * 全エラー表示をクリア
     */
    function clearAllErrors() {
        const errorElements = ['roomNameError', 'roomDescError', 'maxMembersError', 'roomPasswordError'];
        errorElements.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = '';
                element.style.display = 'none';
            }
        });

        // is-invalid クラスを削除
        const inputs = createRoomForm.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.classList.remove('is-invalid');
        });
    }

    /**
     * エラー表示
     */
    function displayErrors(errors) {
        const errorMappings = {
            'room_name': 'roomNameError',
            'room_description': 'roomDescError',
            'max_members': 'maxMembersError',
            'room_password': 'roomPasswordError'
        };

        for (const [field, messages] of Object.entries(errors)) {
            const errorElementId = errorMappings[field];
            const errorElement = document.getElementById(errorElementId);
            const inputElement = createRoomForm.querySelector(`[name="${field}"]`);

            if (errorElement && messages.length > 0) {
                errorElement.textContent = messages[0];
                errorElement.style.display = 'block';
            }

            if (inputElement) {
                inputElement.classList.add('is-invalid');
            }
        }
    }

    /**
     * バリデーションUI更新
     */
    function updateValidationUI(isValid, errorMessage) {
        // エラーメッセージ表示領域を取得または作成
        let errorDiv = document.getElementById('room-form-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'room-form-error';
            errorDiv.className = 'alert alert-danger mt-2';
            errorDiv.style.display = 'none';
            roomNameInput.parentNode.appendChild(errorDiv);
        }

        if (!isValid && errorMessage) {
            errorDiv.textContent = errorMessage;
            errorDiv.style.display = 'block';
            roomNameInput.classList.add('is-invalid');
        } else {
            errorDiv.style.display = 'none';
            roomNameInput.classList.remove('is-invalid');
        }
    }

    // フォーム送信時の処理
    if (createRoomForm) {
        createRoomForm.addEventListener('submit', function(event) {
            // バリデーションチェック
            if (createRoomBtn && createRoomBtn.disabled) {
                event.preventDefault();
                if (typeof swal_alert === 'function') {
                    swal_alert('入力エラー', 'フォームに不正な値が入力されています。内容を確認してください。', 'warning');
                }
                return false;
            }
        });
    }

    // フラッシュメッセージの処理（SweetAlert2で表示）
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        const messageText = message.textContent.trim();
        const isSuccess = message.classList.contains('alert-success');
        const isError = message.classList.contains('alert-danger') || message.classList.contains('alert-error');

        if (messageText && (isSuccess || isError)) {
            // 元のメッセージを非表示
            message.style.display = 'none';

            // SweetAlert2で表示
            if (typeof swal_alert === 'function') {
                if (isSuccess) {
                    swal_alert('成功', messageText, 'success', function() {
                        // 成功時はBootstrap Tableを更新
                        refreshBootstrapTable();
                    });
                } else if (isError) {
                    swal_alert('エラー', messageText, 'error');
                }
            } else {
                // フォールバック
                alert(messageText);
            }
        }
    });
});
