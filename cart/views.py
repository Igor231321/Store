from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from cart.models import Cart
from cart.services import check_quantity
from cart.utils import get_user_carts
from product.models import ProductVariation


def cart_add(request):
    variation_id = int(request.POST.get("variation_id"))
    quantity = int(request.POST.get("quantity"))

    product_variation = ProductVariation.objects.get(id=variation_id)
    variation_quantity = product_variation.quantity

    carts_query = {"product_variation": product_variation}
    context = {"carts": get_user_carts(request)}

    if request.user.is_authenticated:
        carts_query["user"] = request.user
    else:
        carts_query["session_key"] = request.session.session_key

    carts = Cart.objects.filter(**carts_query)

    if carts.exists():
        cart = carts.first()
        new_quantity = cart.quantity + quantity

        result = check_quantity(variation_quantity, new_quantity)
        cart.quantity = result["quantity"]
        context["message"] = result["message"]
        context["cart_id"] = cart.id
        cart.save()
    else:
        result = check_quantity(variation_quantity, quantity)
        carts_query["quantity"] = result["quantity"]
        context["message"] = result["message"]
        cart = Cart.objects.create(**carts_query)
        context["cart_id"] = cart.id

    context["variation_quantity"] = variation_quantity

    # if referer page is create_order add key orders: True to context
    referer = request.META.get("HTTP_REFERER")
    if reverse("order:create") in referer:
        context["order"] = True

    cart_items_html = render_to_string(
        "cart/includes/included_cart.html", context, request=request
    )

    response_data = {
        "cart_items_html": cart_items_html,
        "carts_quantity": carts.total_quantity(),
    }
    return JsonResponse(response_data)


def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = int(request.POST.get("quantity"))
    increment = request.POST.get("increment")

    carts = get_user_carts(request)
    context = {"carts": carts}
    cart = Cart.objects.get(id=cart_id)
    if increment:
        result = check_quantity(variation_quantity=cart.product_variation.quantity, quantity=quantity)
        cart.quantity = result.get("quantity")
        message = result.get("message")
        context.update({"message": message, "cart_id": cart.id})
    else:
        cart.quantity = quantity
    cart.save()


    cart_items_html = render_to_string(
        "cart/includes/included_cart.html", context, request=request
    )

    response_data = {
        "cart_items_html": cart_items_html,
        "carts_quantity": carts.total_quantity(),
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
