from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from cart.models import Cart
from product.models import ProductVariation


def cart_add(request):
    variation_id = request.POST.get("variation_id")
    quantity = int(request.POST.get("quantity"))

    product_variation = ProductVariation.objects.get(id=variation_id)

    carts = Cart.objects.filter(user=request.user, product_variation=product_variation)

    if carts.exists():
        cart = carts.first()
        cart.quantity += quantity
        cart.save()
    else:
        Cart.objects.create(
            user=request.user, product_variation=product_variation, quantity=quantity
        )

    carts = Cart.objects.filter(user=request.user)
    cart_items_html = render_to_string(
        "cart/includes/included_cart.html", {"carts": carts}, request=request
    )

    response_data = {
        "cart_items_html": cart_items_html,
    }
    return JsonResponse(response_data)


def cart_remove(request):
    cart_id = request.POST.get("cart_id")

    cart = get_object_or_404(Cart, id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = Cart.objects.filter(user=request.user)
    cart_items_html = render_to_string(
        "cart/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {"cart_items_html": cart_items_html, "quantity_deleted": quantity}
    return JsonResponse(response_data)
