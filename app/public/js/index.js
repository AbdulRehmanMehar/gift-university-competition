$(document).ready(() => {
    let app_uri = $('meta[name="base_uri"]').attr('content');
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

    $('#save-cart').click((event) => {
        event.preventDefault();
        let title = prompt("Enter title for the cart: ");
        if (title) {
            $.ajax({
                type: 'POST',
                url: `${app_uri}/save-cart`,
                data: {
                    title: title
                },
                success: () => window.location.reload(),
                error: (error) => console.error(error)
            })
        }
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

    $('.cart-update-form').each((i, el) => {
        $(el).submit(event => {
            event.preventDefault();
            let qtty = $(event.target).find($('input[type=number]')).val();
            let pslug = $(event.target).find($('input[type=hidden]')).val();
            updateTheCart(qtty, pslug);
        });
    });

    $('.delete-cart-item').each((i, el) => {
        $(el).click((event) => {
            event.preventDefault();
            let pslug = $(event.target).find($('.sr-only')).html();
            deleteFromCart(pslug);
        });
    });

    $('.delete-db-cart').each((i, el) => {
        $(el).click(event => {
            event.preventDefault();
            let id = $(event.target).attr('cart-id');
            $.ajax({
                type: 'POST',
                url: `${app_uri}/delete-db-cart`,
                data: {
                    id: id
                },
                success: () => window.location.reload(),
                error: (error) => console.error(error)
            })
        });
    });

    function addToCart(qtty, pslug) {
        let cartItems = $('#cart_items');
        $.ajax({
            type: 'POST',
            url: `${app_uri}/add-to-cart/${pslug}`,
            data: {
                quantity: qtty
            },
            success: () => updateCartLength(),
            error: (msg) => console.error(msg)
        });
    }


    function updateTheCart(qtty, pslug) {
        $.ajax({
            type: 'POST',
            url: `${app_uri}/update-cart/${pslug}`,
            data: {
                quantity: qtty
            },
            success: () => {
                let old_qtty = parseInt($(`#${pslug}-qtty`).html());
                let price = parseInt($(`#${pslug}-price`).html());
                let gtotal = parseInt($('#g-total').html());
                let total = price * qtty;
                $(`#${pslug}-qtty`).html(qtty);
                $(`#${pslug}-total`).html(total);
                $('#g-total').html((gtotal - (price * old_qtty)) + total);
                updateCartLength();
            },
            error: (msg) => console.error(msg)
        })
    }

    function deleteFromCart(pslug) {
        $.ajax({
            type: 'POST', 
            url: `${app_uri}/remove-from-cart/${pslug}`,
            success: () => {
                let old_qtty = parseInt($(`#${pslug}-qtty`).html());
                let price = parseInt($(`#${pslug}-price`).html());
                let gtotal = parseInt($('#g-total').html());
                $('#g-total').html(gtotal - (price * old_qtty));
                $(`#tr-${pslug}`).remove();
                updateCartLength();
            },
            error: (msg) => console.error(msg)
        })
    }

    function updateCartLength() {
        let cartItems = $('#cart_items');
        $.ajax({
            type: 'POST',
            url: `${app_uri}/cart-len`,
            success: (len) => {
                $(cartItems).html(len);
            }
        });
    }

});