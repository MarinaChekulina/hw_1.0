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


// /*Ajax отправка формы*/
//     $('.form_subscr').on('submit', function (event) {
//         event.preventDefault();
//         var channel_id = parseInt($('.channel_id').text());
//
//         $.ajax({
//             url: '/subscribe/'+ channel_id,
//             type: 'POST',
//             dataType: 'json',
//             data: {
//                 'csrfmiddlewaretoken': $('.form_subscr input[name=csrfmiddlewaretoken]').val()
//             },
//             error: function () {
//                 console.log('Error!')
//             },
//             success: function (data) {
//                 $('.users').append('<p class="list_users">' + data.message + '</p>');
//             }
//         });
//     });











// /*
//  * На сколько страниц автоматически прокручиваем до остановки
//  */
// var maxPages = 3;
// /*
//  * За сколько до конца страницы включаем прокрутку
//  */
// var scrollBufferRatio = 1 / 3;
// /*
//  * Где находится область для дополнения (содержимое)
//  */
// var elementContainerSelector = '.messages';
// /*
//  * Что делать если не найден новое содержимое
//  */
// var elementFindingErrorHandler = function() {
//     throw "Could not find " + elementContainerSelector;
// };
//
// /*
//  * Названия события которое можно изменить
//  * если есть несколько областей прокрутки
//  */
// var eventName = 'scroll.toInfinity';
// /*
//  * Где находится выбор страниц для перехода
//  */
// var pagerSelector = '.pager';
// /*
//  * Где найти ссылку на следующую страницу
//  */
// var nextPageSelector = '.pager .nextpage';
//
// var $window = $(window);
// // инициализируем при загрузке страницы
// var $elementContainer;
// var topOffset = 0,
//     scrollBuffer = 1,
//     pageCounter = 1;
//
// var eventProcessor = function(finished) {
//     // позиция прокрутки когда должна сработать загрузка
//     // считается от фактической высоты содержимого
//     var triggerPosition = $elementContainer.height()
//             + topOffset - scrollBuffer;
//     // текущая позиция прокрутки по нижней части окна
//     var scrollPosition = $window.scrollTop() + $window.height();
//
//     // еще не дошли до нужной точки, ничего не делаем
//     if (scrollPosition < triggerPosition) {
//         // но ждём дальше
//         finished();
//         return true;
//     }
//
//     // пролистали достаточное число страниц
//     if (pageCounter >= maxPages) {
//         // дадим выбор пользователю листать ли дальше
//         $(pagerSelector).show();
//         // не перезапускаем загрузку
//         return true;
//     }
//
//     // если следующей страницы нет...
//     var $nextPage = $(nextPageSelector);
//     if ($nextPage.length == 0) {
//         // то и загружать дальше нечего
//         return true;
//     }
//
//     $.get($nextPage.attr('href'), function(data) {
//         var $data = $(data);
//
//         // найдем содержимое в следующей странице
//         var $newContent = $data.find(elementContainerSelector);
//         if ($newContent.length == 0) {
//             // если элемент не найден, он может быть корневым
//             $newContent = $data.filter(elementContainerSelector);
//         }
//         // если ничего не найдено, то это конкретно ошибка
//         if ($newContent.length == 0) {
//             elementFindingErrorHandler();
//         }
//
//         // содержимое из следующей страницы допишем
//         // к содержимому страницы в окне
//         $elementContainer.append($newContent.first().html());
//
//         // найдем выбор страниц на следующей странице
//         var $newPager = $data.find(pagerSelector);
//         if ($newPager.length == 0) {
//             // корневой элемент тоже поищем
//             $newPager = $data.filter(pagerSelector);
//         }
//         // заменим выбор страниц новым
//         var newPager = $newPager.first().html();
//         // и скроем его пока не будет нужен
//         $(pagerSelector).html(newPager).hide();
//
//     }).always(function() {
//         pageCounter += 1;
//         // по окончании загрузки снова следим за прокруткой
//         finished();
//     });
// };

// var eventTimeout = 0;
//
// var eventHandler = function() {
//     // событие на прокрутку должно сработать только один раз
//     $window.unbind(eventName);
//     clearTimeout(eventTimeout);
//     eventTimeout = setTimeout(function() {
//         // возьмем небольшую паузу чтобы не считать оставшиеся
//         // пиксели при каждом событии прокрутки
//         eventProcessor(function() {
//             // после окончания загрузки снова ждем прокрутки
//             $window.bind(eventName, eventHandler);
//         });
//     }, 100);
// };
//
// $(function() {
//     $elementContainer = $(elementContainerSelector);
//     // расстояния до элемента от верха экрана
//     topOffset = $elementContainer.offset().top;
//     // зададим пропорционально изначальной высоте
//     scrollBuffer = $elementContainer.height() * scrollBufferRatio;
//     $window.bind(eventName, eventHandler);
// });
