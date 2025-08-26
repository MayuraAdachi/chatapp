$(function () {
    //  パスワード表示/非表示の切り替え
    let viewicon = document.getElementById('pass_view');
    let inputtype = document.getElementById('password');

    if (viewicon && inputtype) {
        $('#pass_view').on('click', function () {
            if(inputtype.type === 'password'){
                inputtype.type = 'text';
                viewicon.innerHTML = '<i class="far fa-eye"></i>';
            } else {
                inputtype.type = 'password';
                viewicon.innerHTML = '<i class="far fa-eye-slash"></i>';
            }
        });
    }
});
