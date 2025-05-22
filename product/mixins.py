class ProductOrderByMixin:
    @staticmethod
    def filters(queryset, order_by):
        if order_by and order_by != "default":
            return queryset.order_by(order_by)
        else:
            return queryset
