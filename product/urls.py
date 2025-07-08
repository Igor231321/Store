from django.urls import path

from product import views

app_name = "product"

urlpatterns = [
    path("", views.home),
    path('upload-products/', views.UploadData.as_view(), name='upload_products'),
    path("product/<slug:slug>/", views.ProductDetail.as_view(), name="detail"),
    path("сategories/", views.CategoryListView.as_view(), name="сategories"),
    path("category/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("variation_data/", views.variation_data, name="variation_data"),
    path("search_data/", views.ProductSearch.as_view(), name="search_data"),
    path("search_list/", views.ProductSearchTemplateView.as_view(), name="search_list"),
 ]
