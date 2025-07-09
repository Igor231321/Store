from django.urls import path

from user import views

app_name = "user"


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("account/", views.UserAccountView.as_view(), name="account"),
    path("user_orders/", views.UserOrders.as_view(), name="user_orders"),
    path("password-change/", views.UserPasswordChangeView.as_view(), name="password_change"),
]
