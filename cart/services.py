from django.utils.translation import gettext_lazy as _


def check_quantity(variation_quantity, quantity):
    if quantity > variation_quantity:
        message = _(f"На складі лише {variation_quantity} шт., кількість автоматично зменшена")
        quantity = variation_quantity
    else:
        message = ""

    return {"quantity": quantity, "message": message}
