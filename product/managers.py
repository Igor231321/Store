from django.db.models import Max, Min, QuerySet


class ProductQuerySet(QuerySet):
    def with_min_max_prices(self):
        return self.annotate(
            min_price=Min("variations__price"), max_price=Max("variations__price")
        )
