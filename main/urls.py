from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("<slug:slug>/", views.PageDetailView.as_view(), name="page_detail"),
    path("", views.HomeTemplateView.as_view(), name="home"),
]
