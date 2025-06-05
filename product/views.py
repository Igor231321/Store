import csv

from django.http import JsonResponse
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
            Product.objects.with_min_max_prices().filter(brand=self.get_object().brand)
            .exclude(pk=self.get_object().pk)[:4]
        )

        variation_article = self.request.GET.get("variation_article", None)
        if variation_article:
            context["variation"] = ProductVariation.objects.get(article=variation_article)
            context["variation_article"] = variation_article
        else:
            context["variation"] = self.get_object().variations.first()

        return context


def variation_data(request):
    article = request.GET.get("variation_article")
    variation = ProductVariation.objects.get(article=article)
    data = {
        "variation_id": variation.id,
        "article": variation.article,
        "price": f"{variation.get_price()} грн.",
        "price_with_discount": f"{variation.get_price_with_discount()} грн.",
        "characteristics": list(variation.characteristics.values("name", "value"))
    }
    return JsonResponse(data)


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
