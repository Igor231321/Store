from django.urls import path

from api.views import OrderListAPIView

app_name = "api"


urlpatterns = [
    path("order_list/", OrderListAPIView.as_view(), name="order_list"),
]
