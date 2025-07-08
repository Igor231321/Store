from rest_framework import serializers

from order.models import Order, OrderItem
from product.serializers import ProductVariationDetailSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_variation = ProductVariationDetailSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product_variation", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "session_key", "status", "first_name", "last_name", "phone_number", "surname", "email",
                  "delivery_method", "created_at",
                  "np_country", "np_warehouse", "np_terminal",
                  "ukr_address", "ukr_post_code",
                  "meest_country", "meest_warehouse",
                  "comment", "do_not_call", "items"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["delivery_method"] = instance.get_delivery_method_display()
        data["status"] = instance.get_status_display()
        return data
