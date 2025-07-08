from rest_framework import serializers

from product.models import Category, Product, ProductVariation


class ProductShortSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "category", "brand", "discount"]


class ProductVariationShortSerializer(serializers.ModelSerializer):
    attribute_value = serializers.SlugRelatedField(slug_field="value", read_only=True)

    class Meta:
        model = ProductVariation
        fields = ["id", "attribute_value", "article", "get_price", "get_price_with_discount"]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)
    variations = ProductVariationShortSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "category", "brand", "discount", "variations", "get_absolute_url"]


class ProductVariationDetailSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)
    attribute_value = serializers.SlugRelatedField(slug_field="value", read_only=True)

    class Meta:
        model = ProductVariation
        fields = ["id", "product", "attribute_value", "article", "get_price", "get_price_with_discount"]


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    products = ProductDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "image", "children", "products"]

    def get_children(self, obj):
        children = obj.get_children()
        return CategorySerializer(children, many=True).data
