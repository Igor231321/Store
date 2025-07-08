from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser

from order.models import Order
from order.serializers import OrderSerializer
from product.models import Category
from product.serializers import CategorySerializer


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.root_nodes()


class CategoryDetailAPIView(RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
