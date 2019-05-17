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

    $('#showCartButton').click(() => {
        $('#cart-form').toggleClass('active');
    });

    $('#cart-form').submit((event) => {
        event.preventDefault();
        let qtty = $('#cart-form #cart-qtty').val();
        let pslug = $('#cart-form #product-slug').val();
        addToCart(qtty, pslug);
    });

    $('.add-to-cart-from').each((i, el) => {
        $(el).submit((event) => {
            event.preventDefault();
            let qtty = $(event.target).find($('input[type=number]')).val();
            let pslug = $(event.target).find($('input[type=hidden]')).val();
            addToCart(qtty, pslug);
        });
    });

    function addToCart(qtty, pslug) {
        let cartItems = $('#cart_items');
        $.ajax({
            type: 'POST',
            url: 'http://localhost:5000/add-to-cart/' + pslug,
            data: {
                quantity: qtty
            },
            success: (data) => {
                let n = parseInt($(cartItems).html()) + parseInt(qtty);
                $(cartItems).html(n);
            },
            error: (msg) => console.error(msg)
        });
    }

});