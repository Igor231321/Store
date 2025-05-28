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

        price_before_discount = ExpressionWrapper(F("variations__price") * currency_rate,
                                                  output_field=DecimalField(max_digits=10, decimal_places=2))

        price_after_discount = ExpressionWrapper(price_before_discount * discount,
                                       output_field=DecimalField(max_digits=10, decimal_places=2))

        return self.annotate(
            min_price_before_discount=Min(price_before_discount),
            max_price_before_discount=Max(price_before_discount),
            min_price_after_discount=Min(price_after_discount),
            max_price_after_discount=Max(price_after_discount)
        )
