import csv

from django.db.models import Max, Min
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic

from product.forms import UploadDataForm
from product.models import Color, Product, ProductVariation


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
    paginate_by = 99

    def get_queryset(self):
        products = Product.objects.annotate(
            min_price=Min("variations__price"), max_price=Max("variations__price")
        )

        selected_colors = self.request.GET.getlist("color")
        if selected_colors:
            products = products.filter(variations__color__slug__in=selected_colors)

        min_price = self.request.GET.get("min_price", None)
        if min_price:
            products = products.filter(variations__price__gte=min_price)

        max_price = self.request.GET.get("max_price", None)
        if max_price:
            products = products.filter(variations__price__lte=max_price)

        order_by = self.request.GET.get("order_by", None)
        if order_by and order_by != "default":
            products = products.order_by(order_by)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.all()
        context["colors"] = Color.objects.filter(
            variations__product__in=products
        ).distinct()
        context["selected_colors"] = self.request.GET.getlist("color")

        product_prices = ProductVariation.objects.aggregate(Min("price"), Max("price"))
        context["min_price"] = product_prices["price__min"]
        context["max_price"] = product_prices["price__max"]

        return context


class ProductDetail(generic.DetailView):
    template_name = "product/detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs["slug"])
