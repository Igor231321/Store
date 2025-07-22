import csv

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, FormView, ListView, TemplateView

from django.utils.translation import gettext_lazy as _
from order.forms import QuickOrderForm
from product.forms import ReviewForm, UploadDataForm
from product.mixins import ProductOrderByMixin
from product.models import Category, Product, ProductVariation
from product.services.product_search import product_search


class HomeTemplateView(TemplateView):
    template_name = "product/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()
        context["popular_products"] = Product.objects.with_min_max_prices()
        return context


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

        context["form"] = QuickOrderForm()
        context["variation"] = self.get_object().variations.first()
        context["review_form"] = ReviewForm()

        return context


def variation_data(request):
    article = request.GET.get("variation_article")
    variation = ProductVariation.objects.get(article=article)
    characteristics = render_to_string("product/includes/variation_characteristics.html",
                                       {"characteristics": variation.characteristics.values("name", "value")})
    reviews = render_to_string("product/includes/variation_reviews.html",
                               {"reviews": variation.reviews.all()})
    data = {
        "variation_id": variation.id,
        "article": variation.article,
        "price": f"{variation.get_price()} грн.",
        "price_with_discount": f"{variation.get_price_with_discount()} грн.",
        "characteristics": characteristics,
        "reviews": reviews,
        "in_stock": variation.status == "IN_STOCK"
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


class ProductSearch(View):
    def get(self, request, *args, **kwargs):
        q = self.request.GET.get("q", "")
        products = product_search(query=q)

        context = {"products": products}
        html = render_to_string("product/includes/search_results.html", context)
        return JsonResponse({"html": html})


class ProductSearchTemplateView(TemplateView):
    template_name = "product/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get("q", "")
        context["products"] = product_search(query=q)

        return context


@require_POST
def review_form(request):
    variation_id = request.POST.get("variation_id")
    variation = ProductVariation.objects.get(id=variation_id)
    rating = request.POST.get("rating")

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product_variation = variation
        review.rating = int(rating)
        review.save()
        messages.success(request, _("Відгук успішно додано"))
        return redirect(request.META.get("HTTP_REFERER", "/"))

    return redirect(request.META.get("HTTP_REFERER", "/"))
