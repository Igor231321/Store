"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("cart/", include("cart.urls", namespace="cart")),
    path("order/", include("order.urls", namespace="order")),
    path("user/", include("user.urls", namespace="user")),
    path("api/", include("api.urls", namespace="api")),
    path("api-token-auth/", views.obtain_auth_token),
    path("products/", include("product.urls", namespace="product")),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("", include("main.urls", namespace="main"))
)

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
