$(document).ready(() => {
    let href = window.location.href.split('/').pop();
    $('.nav-link').each((i, el) => {
        let hr = $(el).attr('href').split('/').pop();
        if(href === hr) $(el).parent().addClass('active');
    });

    $('textarea').each((i, el) => {
        if($(el).attr('html_')) {
            $(el).html($(el).attr('html_'));
        }
    });

});