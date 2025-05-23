import csv

from django.db.models import Max, Min
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from product.forms import UploadDataForm
from product.mixins import ProductOrderByMixin
from product.models import Category, Product, ProductVariation


def home(request):
    return render(request, "product/index.html")


class UploadData(FormView):
    template_name = "product/upload_data.html"
    form_class = UploadDataForm
    success_url = reverse_lazy("admin:index")

    def form_valid(self, form):
        csv_file = form.cleaned_data["csv_file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            Product.objects.create(
                name=row["name"],
                description=row["description"],
                slug=row["slug"],
                quantity=row["stock"],
            )
        return super().form_valid(form)


class Catalog(ProductOrderByMixin, ListView):
    template_name = "product/catalog.html"
    context_object_name = "products"
    model = Product
    paginate_by = 6

    def get_queryset(self):
        products = Product.objects.with_min_max_prices()

        min_price = self.request.GET.get("min_price", None)
        if min_price:
            products = products.filter(variations__price__gte=min_price)

        max_price = self.request.GET.get("max_price", None)
        if max_price:
            products = products.filter(variations__price__lte=max_price)

        order_by = self.request.GET.get("order_by", None)
        products = self.filters(products, order_by)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_prices = ProductVariation.objects.aggregate(Min("price"), Max("price"))
        context["min_price"] = product_prices["price__min"]
        context["max_price"] = product_prices["price__max"]

        return context


class ProductDetail(DetailView):
    template_name = "product/detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["has_attribute"] = (
            self.get_object().variations.filter(attribute_value__isnull=False).exists()
        )
        context["products_brand"] = (
            Product.objects.filter(brand=self.get_object().brand)
            .exclude(pk=self.get_object().pk)
            .annotate(
                min_price=Min("variations__price"), max_price=Max("variations__price")
            )[:4]
        )
        return context


class CategoryListView(ListView):
    model = Category
    template_name = "product/categories.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.root_nodes()


class CategoryDetailView(ProductOrderByMixin, DetailView):
    model = Category
    template_name = "product/category_detail.html"
    context_object_name = "category"

    def get_object(self, queryset=None):
        return get_object_or_404(Category, slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_by = self.request.GET.get("order_by", None)
        category = self.get_object()
        products = category.products.with_min_max_prices()

        context["products"] = self.filters(products, order_by)
        context["subcategories"] = category.get_children()
        return context
