from cart.models import Cart


def transfer_session_cart_to_user(request, user):
    session_key = request.session.session_key

    if session_key:
        Cart.objects.filter(session_key=session_key).update(user=user)
