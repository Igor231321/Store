from django.db.models import F, Max, Min, QuerySet, ExpressionWrapper, Value, DecimalField
from django.db.models.functions import Round, Coalesce


class ProductQuerySet(QuerySet):
    def with_min_max_prices(self):
        currency_rate = Coalesce(F("currency__rate"), 1)

        price_expr = ExpressionWrapper(F("variations__price") * currency_rate,
                                       output_field=DecimalField(max_digits=10, decimal_places=2))

        return self.annotate(
            min_price=Min(price_expr),
            max_price=Max(price_expr)
        )
