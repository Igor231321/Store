from rest_framework.generics import ListAPIView

from order.models import Order
from order.serializers import OrderSerializer


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
