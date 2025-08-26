// jQueryプラグイン化：requiredバリデーション（data-required/data-title対応）
(function($) {
    $.fn.validateRequiredFields = function(options) {
        const settings = $.extend({
            errorClass: 'error-message',
            errorText: '必須項目です'
        }, options);
        let isValid = true;
        this.find('.' + settings.errorClass).remove();
        // data-required="true"属性を持つ要素を対象
        this.find('input[data-required="true"], textarea[data-required="true"], select[data-required="true"]').each(function() {
            if (!$.trim($(this).val())) {
                let msg = settings.errorText;
                const title = $(this).data('title');
                if (title) {
                    msg = title + 'は必須項目です。';
                }
                if (!$(this).next().hasClass(settings.errorClass)) {
                    $('<div>').addClass(settings.errorClass).text(msg).insertAfter($(this));
                }
                isValid = false;
            }
        });
        return isValid;
    };
    $(function() {
        $('form').on('submit', function(e) {
            if (!$(this).validateRequiredFields()) {
                e.preventDefault();
            }
        });
    });
})(jQuery);
