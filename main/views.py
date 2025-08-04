from django.core.cache import cache
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView

from main.models import Page, Slider
from product.models import Category, Product, ProductVariation


class HomeTemplateView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cached = cache.get_many(["categories", "popular_products", "sliders"])

        categories = cached.get("categories")
        popular_products = cached.get("popular_products")
        sliders = cached.get("sliders")

        to_cache = {}

        if not categories:
            categories = Category.objects.filter(in_home_page=True)
            to_cache["categories"] = categories

        if not popular_products:
            popular_products = Product.objects.filter(in_home_page=True).prefetch_related(
                Prefetch("variations", queryset=ProductVariation.objects.select_related("attribute_value"))
            ).with_min_max_prices()
            to_cache["popular_products"] = popular_products

        if not sliders:
            sliders = Slider.objects.filter(is_active=True)
            to_cache["sliders"] = sliders

        if to_cache:
            cache.set_many(to_cache, timeout=60 * 5)

        context["categories"] = categories
        context["popular_products"] = popular_products
        context["sliders"] = sliders
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = "main/page_detail.html"

    def get_object(self, queryset=None):
        page_slug = self.kwargs["slug"]
        page = cache.get_or_set(f"page_{page_slug}", lambda: get_object_or_404(Page, slug=page_slug), 60 * 10)

        return page
