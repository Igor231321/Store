import hashlib
import hmac

from django.conf import settings


def get_signature(base_string):
    signature = hmac.new(
        settings.WAYFORPAY_SECRET_KEY.encode("utf-8"),
        base_string.encode("utf-8"),
        hashlib.md5
    ).hexdigest()

    return signature


def generate_signature(order_data):
    parts = [
        "test_merch_n1",
        "127.0.0.1",
        order_data["orderReference"],
        str(int(order_data["orderDate"])),
        str(order_data["amount"]),
        order_data["currency"],
        *order_data["productName"],
        *map(str, order_data["productCount"]),
        *map(str, order_data["productPrice"]),
    ]

    base_string = ";".join(parts)

    signature = get_signature(base_string)

    return signature
