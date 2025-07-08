from django.db.models import Q

from product.models import Product


def product_search(query):
    keywords = [word for word in query.split() if len(word) > 1]

    queryset = Product.objects.with_min_max_prices()

    if not keywords:
        return Product.objects.none()

    for token in keywords:
        queryset = queryset.filter(
            Q(name__icontains=token) |
            Q(variations__article__icontains=token)
        )

    return queryset
