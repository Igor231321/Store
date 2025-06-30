from rest_framework import serializers

from order.models import Order, OrderItem
from product.models import ProductVariation, Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)
    currency = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Product
        fields = ["name", "category", "brand", "currency", "discount"]


class ProductVariationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    attribute_value = serializers.SlugRelatedField(slug_field="value", read_only=True)

    class Meta:
        model = ProductVariation
        fields = ["id", "product", "attribute_value", "article", "get_price", "get_price_with_discount"]


class OrderItemSerializer(serializers.ModelSerializer):
    product_variation = ProductVariationSerializer(read_only=True)

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
