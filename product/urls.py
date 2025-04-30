from django.urls import path

from product import views

app_name = "product"

urlpatterns = [
    path("", views.home),
    path('upload-products/', views.UploadData.as_view(), name='upload_products'),
    path("catalog/", views.Catalog.as_view(), name="catalog"),
    path("product/<slug:slug>/", views.ProductDetail.as_view(), name="detail")
 ]
