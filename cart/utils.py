from cart.models import Cart


def get_user_carts(request=None, user=None, session_key=None):
    filters = {}

    if user:
        filters["user"] = user
    elif session_key:
        filters["session_key"] = session_key
    else:
        if request.user.is_authenticated:
            filters["user"] = request.user
        else:
            if not request.session.session_key:
                request.session.create()
            filters["session_key"] = request.session.session_key

    carts = Cart.objects.filter(**filters).select_related("product_variation",
                                                          "product_variation__product",
                                                          "product_variation__attribute_value__attribute",
                                                          "product_variation__attribute_value")
    return carts
