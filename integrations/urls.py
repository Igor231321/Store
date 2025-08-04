from django.urls import path

from integrations import views

app_name = "integrations"


urlpatterns = [
    path("wayforpay_callback/", views.wayforpay_callback, name="wayforpay_callback"),
]
