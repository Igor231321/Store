import json
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from cart.utils import get_user_carts
from integrations.services.wayforpay_services import get_signature
from order.models import Order, OrderItem


@csrf_exempt
def wayforpay_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # 1. Отримуємо дані
        order_reference = data.get("orderReference")
        amount = data.get("amount")
        currency = data.get("currency")
        auth_code = data.get("authCode")
        card_pan = data.get("cardPan")
        transaction_status = data.get("transactionStatus")
        reason_code = data.get("reasonCode")
        received_signature = data.get("merchantSignature")

        # 2. Формуємо рядок для підпису
        signature_base = (f"{data.get('merchantAccount')};{order_reference};{amount};{currency};"
                          f"{auth_code};{card_pan};{transaction_status};{reason_code}")

        # 3. Обчислюємо HMAC_MD5
        expected_signature = get_signature(signature_base)

        if received_signature != expected_signature:
            return JsonResponse({"error": "Invalid signature"}, status=400)

        # 4. Якщо транзакція успішна — оновити замовлення або додати товари
        if transaction_status == "Approved":
            order = Order.objects.get(reference=order_reference)

            order.paid = True
            order.save()

            user_carts = get_user_carts(user=order.user, session_key=order.session_key)

            for cart in user_carts:
                OrderItem.objects.create(
                    order=order,
                    product_variation=cart.product_variation,
                    quantity=cart.quantity,
                )

            user_carts.delete()

        # 5. Сформувати відповідь
        response_time = int(time.time())
        status = "accept"
        response_signature_str = f"{order_reference};{status};{response_time}"
        response_signature = get_signature(response_signature_str)

        return JsonResponse({
            "orderReference": order_reference,
            "status": status,
            "time": response_time,
            "signature": response_signature,
        })

    return JsonResponse({"error": "Invalid method"}, status=405)
