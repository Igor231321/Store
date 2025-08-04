from django.urls import path

from order import views

app_name = "order"


urlpatterns = [
    path("detail/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("create/", views.OrderCreateView.as_view(), name="create"),
    path("get_countries/", views.get_countries, name="get_countries"),
    path("get_warehouses/", views.get_warehouses, name="get_warehouses"),
    path("quick_order_form/", views.quick_order_form, name="quick_order_form"),
    path("thanks_order/", views.thanks_order, name="thanks_order")
]
