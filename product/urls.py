from django.urls import path

from product import views

app_name = "product"

urlpatterns = [
    path("", views.home),
    path('upload-products/', views.UploadData.as_view(), name='upload_products'),
    path("product/<slug:slug>/", views.ProductDetail.as_view(), name="detail"),
    path("сategories/", views.CategoryListView.as_view(), name="сategories"),
    path("category/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail")
 ]
