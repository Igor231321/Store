from django.urls import path

from api.views import (CategoryDetailAPIView, CategoryListAPIView,
                       OrderListAPIView)

app_name = "api"


urlpatterns = [
    path("order_list/", OrderListAPIView.as_view(), name="order_list"),
    path("category_list/", CategoryListAPIView.as_view(), name="category_list"),
    path("category_detail/<int:pk>/", CategoryDetailAPIView.as_view(), name="category_detail")
]
