from django.db.models import (DecimalField, ExpressionWrapper, F, Max, Min,
                              QuerySet)
from django.db.models.functions import Coalesce


class ProductQuerySet(QuerySet):
    def with_min_max_prices(self):
        # Беремо знижку (У відсотках), якщо немає, то 0
        variation_discount = Coalesce(F("discount"), 0)

        # Беремо курс, якщо немає, то 1
        currency_rate = Coalesce(F("currency__rate"), 1)

        # Обчислюємо множник знижки: (1 - discount/100)
        discount = 1 - variation_discount / 100

        price_expr = ExpressionWrapper(F("variations__price") * currency_rate * discount,
                                       output_field=DecimalField(max_digits=10, decimal_places=2))

        return self.annotate(
            min_price=Min(price_expr),
            max_price=Max(price_expr)
        )
