/**
 * Created by Марина on 28.12.2016.
 */
$(function () {
    function validateForm() {
        $('.text-error').remove();
        var c_title = false;
        var c_image = false;
        var c_category = false;
        var c_text = false;
        var c_video = false;
        var c_date = false;
        var el_t = $('#title');
        if (el_t.val().length > 100) {
            c_title = true;
            $('.channel-title').after('<span class="text-error">Название канала должно быть меньше 100 символов</span>');
        }
        if (el_t.val().length == 0) {
            c_title = true;
            $('.channel-title').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        if ($('form input[type=file]').val().length == 0) {
            c_image = true;
            $('.channel-image').after('<span class="text-error">Выберите файл</span>');
        }

        var el_cat = $('#category');
        if (el_cat.val().length > 50) {
            c_category = true;
            $('.channel-category').after('<span class="text-error">Название категории должно быть меньше 50 символов</span>');
        }
        if (el_cat.val().length == 0) {
            c_category = true;
            $('.channel-category').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        var el_tex = $('#text');
        if (el_tex.val().length == 0) {
            c_text = true;
            $('.channel-text').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        var el_v = $('#video');
        if (el_v.val().length == 0) {
            c_video = true;
            $('.channel-video').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        var el_dat = $('#date');
        if (el_dat.val().length == 0) {
            c_date = true;
            $('.channel-date').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        return (c_title || c_image || c_category || c_text || c_video || c_date);
    }

    $('.add_channel').on('submit', function (event) {
        if (validateForm()) {
            event.preventDefault();
        }
    });

    $('.btn-close').click(function () {
        $('#title').val('');
        $('.text-error').remove();
    });
});













