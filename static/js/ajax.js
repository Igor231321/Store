$(document).ready(function () {

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

        $(document).on("click", ".minus, .plus", function () {
            var $input1 = $("input.product__quantity");
            var $input2 = $("input.product__quantity2");

            var quantity1 = parseInt($input1.val());
            var quantity2 = parseInt($input2.val());

            if ($(this).hasClass("plus")) {
                quantity1 += 1;
                quantity2 += 1;
            } else if ($(this).hasClass("minus") && quantity1 > 1 && quantity2 > 1) {
                quantity1 -= 1;
                quantity2 -= 1;
            }

            $input1.val(quantity1);
            $input2.val(quantity2);
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