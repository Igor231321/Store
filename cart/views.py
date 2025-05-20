from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from cart.models import Cart
from cart.utils import get_user_carts
from product.models import Product, ProductVariation


def cart_add(request):
    variation_id = request.POST.get("variation_id")
    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity"))

    if variation_id:
        product_variation = ProductVariation.objects.get(id=variation_id)
    else:
        product = Product.objects.get(id=product_id)
        product_variation = product.variations.first()

    carts_query = {"product_variation": product_variation}

    if request.user.is_authenticated:
        carts_query["user"] = request.user
    else:
        carts_query["session_key"] = request.session.session_key

    carts = Cart.objects.filter(**carts_query)

    if carts.exists():
        cart = carts.first()
        cart.quantity += quantity
        cart.save()
    else:
        carts_query["quantity"] = quantity
        Cart.objects.create(**carts_query)

    context = {"carts": get_user_carts(request)}

    # if referer page is create_order add key orders: True to context
    referer = request.META.get("HTTP_REFERER")
    if reverse("order:create") in referer:
        context["order"] = True

    cart_items_html = render_to_string(
        "cart/includes/included_cart.html", context, request=request
    )

    response_data = {
        "cart_items_html": cart_items_html,
    }
    return JsonResponse(response_data)


def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = int(request.POST.get("quantity"))

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    cart_items_html = render_to_string(
        "cart/includes/included_cart.html", {"carts": get_user_carts(request)}, request=request
    )

    response_data = {
        "cart_items_html": cart_items_html,
        "quaantity": updated_quantity,
    }

    return JsonResponse(response_data)


def cart_remove(request):
    cart_id = request.POST.get("cart_id")

    cart = get_object_or_404(Cart, id=cart_id)
    quantity = cart.quantity
    cart.delete()

    context = {"carts": get_user_carts(request)}

    # if referer page is create_order add key orders: True to context
    referer = request.META.get("HTTP_REFERER")
    if reverse("order:create") in referer:
        context["order"] = True

    cart_items_html = render_to_string(
        "cart/includes/included_cart.html", context, request=request
    )

    response_data = {"cart_items_html": cart_items_html, "quantity_deleted": quantity}
    return JsonResponse(response_data)
