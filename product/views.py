import csv

from django.contrib import messages
from django.core.cache import cache
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, FormView, ListView, TemplateView

from order.forms import QuickOrderForm
from product.forms import InStockNotificationForm, ReviewForm, UploadDataForm
from product.mixins import ProductOrderByMixin
from product.models import Category, Product, ProductVariation
from product.services.product_search import product_search


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
    context_object_name = "product"

    def get_object(self, queryset=None):
        slug = self.kwargs["slug"]
        cache_key = f"product_full_{slug}"

        product = cache.get_or_set(cache_key,
                                   lambda: Product.objects.select_related("brand").prefetch_related(
                                       Prefetch(
                                           "variations",
                                           queryset=ProductVariation.objects
                                           .select_related("attribute_value__attribute")
                                           .prefetch_related("characteristics")
                                           .order_by("price")
                                       )
                                   ).get(slug=slug), 60 * 5)

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.object

        first_variation = self.object.variations.first()
        context["first_variation"] = cache.get_or_set(f"first_variation_{product.id}", first_variation, 60 * 5)

        has_attribute = product.variations.filter(attribute_value__isnull=False)
        context["has_attribute"] = cache.get_or_set(f"has_attribute_{product.id}", has_attribute, 60 * 5)

        products_brand = Product.objects.filter(brand=product.brand).select_related("brand").prefetch_related(
            Prefetch("variations", ProductVariation.objects.select_related("attribute_value"))
        ).with_min_max_prices()[:4]
        context["products_brand"] = cache.get_or_set(f"products_brand_{product.id}", products_brand, 60 * 5)

        # forms
        context["quick_order_form"] = QuickOrderForm()
        context["notification_form"] = InStockNotificationForm()
        context["review_form"] = ReviewForm()

        return context


def variation_data(request):
    article = request.GET.get("variation_article")

    variation_key = f"variation_{article}"
    variation_query = ProductVariation.objects.select_related(
            "attribute_value__attribute", "product"
        ).prefetch_related("characteristics", "reviews").get(article=article)
    variation = cache.get_or_set(variation_key, variation_query, 60 * 5)

    characteristics_key = f"characteristics_{article}"
    characteristics_query = render_to_string("product/includes/variation_characteristics.html",
                                       {"characteristics": variation.characteristics.values("name", "value")})

    characteristics = cache.get_or_set(characteristics_key, characteristics_query, 60 * 5)

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
        query = Category.objects.root_nodes()
        categories = cache.get_or_set("categories_root_nodes", query, 60 * 5)
        return categories


class CategoryDetailView(ProductOrderByMixin, DetailView):
    model = Category
    template_name = "product/category_detail.html"
    context_object_name = "category"

    def get_object(self, queryset=None):
        slug = self.kwargs["slug"]
        query = get_object_or_404(Category, slug=self.kwargs["slug"])
        category = cache.get_or_set(f"category_{slug}", query, 60 * 5)

        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_by = self.request.GET.get("order_by", None)
        category = self.object
        slug = category.slug
        products = Product.objects.select_related("category").filter(category=category).prefetch_related(
            Prefetch("variations", ProductVariation.objects.select_related("attribute_value__attribute"))
        ).with_min_max_prices()

        context["products"] = self.filters(products, order_by) if products else None

        context["subcategories"] = cache.get_or_set(f"subcategories_{slug}", category.get_children, 60 * 5)
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


class InStockNotificationView(View):
    def post(self, *args, **kwargs):
        variation_id = int(self.request.POST.get("variation_id"))
        variation = ProductVariation.objects.get(id=variation_id)

        form = InStockNotificationForm(self.request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product_variation = variation
            messages.success(self.request, _("Дякуємо! Ми повідомимо вас, щойно товар з’явиться в наявності"))
            form.save()

        return redirect(self.request.META.get("HTTP_REFERER", "/"))
