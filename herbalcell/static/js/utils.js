function selectRandomBackground() {
    var n = Math.ceil(Math.random() * 38); // number between 1-38
    var random_bg = n < 10 ? '0' + n : '' + n;
    var new_bg = '/static/images/site-design/bg/' + random_bg + '.jpg';
    if ( $.browser.msie ) {
        var background_img = $('img.background');
        background_img.attr('src', new_bg);
        background_img.show();
    } else {
        $('body').css('background-image', 'url("' + new_bg + '")');
    }
}

function getScrollbarWidth() {
    if ( $.browser.msie ) {
        var $textarea1 = $('<textarea cols="10" rows="2"></textarea>')
                .css({ position: 'absolute', top: -1000, left: -1000 }).appendTo('body'),
            $textarea2 = $('<textarea cols="10" rows="2" style="overflow: hidden;"></textarea>')
                .css({ position: 'absolute', top: -1000, left: -1000 }).appendTo('body');
        scrollbarWidth = $textarea1.width() - $textarea2.width();
        $textarea1.add($textarea2).remove();
    } else {
        var $div = $('<div />')
            .css({ width: 100, height: 100, overflow: 'auto', position: 'absolute', top: -1000, left: -1000 })
            .prependTo('body').append('<div />').find('div')
                .css({ width: '100%', height: 200 });
        scrollbarWidth = 100 - $div.width();
        $div.parent().remove();
    }
    return scrollbarWidth;
};

function scrollFollow() {
    function follow() {
        var sidebar = $(".scroll-follow");
        if ($(window).scrollTop() > 260) {
            sidebar.css({"position": "fixed", "top": "10px"});
        } else {
            sidebar.css({"position": "relative", "top": "0"});
        }
    }
    $(window).scroll(follow);
    follow();
}

function sidebarSort() {
    $('.sort-links').show();
    var sort_links = $('.sort-links a');
    $.fn.toggleSort = function(show_or_hide, remove_or_add_class) {
        $('.sorted-div.' + $(this).attr('id'))[show_or_hide]();
        $(this)[remove_or_add_class]('selected');
    };
    sort_links.click(function() {
        $(this).toggleSort('show', 'addClass');
        sort_links.not($(this)).toggleSort('hide', 'removeClass');
        localStorage.sort_by = $(this).attr('id');
    });
    $('.sort-links a#' + localStorage.sort_by).click();
}

function mobileTabs() {
    $('.tab-wrap').click(function() {
        $('#' + $(this).attr('rel')).show();
        $(this).addClass('selected');
        var unselected = $(this).siblings().first();
        $('#' + unselected.attr('rel')).hide();
        unselected.removeClass('selected');
    });
    if ($('.mobile-tabs').is(':visible')) {
        $('.tab-left').click();
    }
}