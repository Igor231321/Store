$(document).ready(function () {

    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();

        var productsInCartCount = $("#products-in-cart-count");
        var cartCount = parseInt(productsInCartCount.text() || 0);

        var variation_id = $(this).data("variation-id");
        var quantity = parseInt($('.product__quantity').val());

        var add_to_cart_url = $(this).attr("href");

        var postData = {
            variation_id: variation_id,
            quantity: quantity,
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        };

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: postData,
            success: function (data) {
                cartCount += quantity;
                productsInCartCount.text(cartCount);
                $("#cart-items-container").html(data.cart_items_html);
            },
            error: function (data) {
                console.log("Помилка при додаванні товару в кошик", data);
            },
        });
    });

    $(document).on("click", ".remove-from-cart", function (e) {

        e.preventDefault();


        var productsInCartCount = $("#products-in-cart-count");
        var cartCount = parseInt(productsInCartCount.text() || 0);

        var cart_id = $(this).data("cart-id");
        var remove_from_cart = $(this).attr("href");

        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                cartCount -= data.quantity_deleted;
                productsInCartCount.text(cartCount);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },

            error: function (data) {
                console.log("Помилка при додаванні товару в кошик");
            },
        });
    });

    $(document).on("click", '.minus, .plus', function () {
        var $input = $(this).siblings('input.product__quantity');
        var quantity = parseInt($input.val());

        if ($(this).hasClass('plus')) {
            quantity += 1;
        } else if ($(this).hasClass('minus') && quantity > 1) {
            quantity -= 1;
        }

        $input.val(quantity);
    });

    $(document).on("click", ".decrement", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    $(document).on("click", ".increment", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                var productsInCartCount = $("#products-in-cart-count");
                var cartCount = parseInt(productsInCartCount.text() || 0);
                cartCount += change;
                productsInCartCount.text(cartCount);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function (data) {
                console.log("Помилка при додаванні товару в кошик");
            },
        });
    }
}
)