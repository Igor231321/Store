import csv

from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic

from product.forms import UploadDataForm
from product.models import Product


def home(request):
    return render(request, "product/index.html")


class UploadData(generic.FormView):
    template_name = "product/upload_data.html"
    form_class = UploadDataForm
    success_url = reverse_lazy("admin:index")

    def form_valid(self, form):
        csv_file = form.cleaned_data["csv_file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:

            Product.objects.create(
                title=row["name"],
                description=row["description"],
                slug=row["slug"],
                # price=row['price'],
                quantity=row["stock"],
                # article=row['article'],
            )
        return super().form_valid(form)


class Catalog(generic.ListView):
    template_name = "product/catalog.html"
    context_object_name = "products"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context


class ProductDetail(generic.DetailView):
    template_name = "product/detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs["slug"])
