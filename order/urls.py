from django.urls import path

from order import views

app_name = "order"


urlpatterns = [
    path("", views.OrdersListView.as_view(), name="orders"),
    path("detail/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("create", views.OrderCreateView.as_view(), name="create"),
]
