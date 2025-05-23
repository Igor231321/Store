from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from cart.utils import get_user_carts
from order.forms import OrderCreateForm
from order.models import Order, OrderItem
from django.contrib.messages.views import SuccessMessageMixin


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = "order/detail.html"


class OrderCreateView(SuccessMessageMixin, generic.CreateView):
    model = Order
    template_name = "order/create.html"
    form_class = OrderCreateForm
    success_url = reverse_lazy("product:catalog")
    success_message = "Ваше замовлення успішно створено"

    def form_valid(self, form):
        order = form.save(commit=False)
        if self.request.user.is_authenticated:
            order.user = self.request.user
        else:
            order.session_key = self.request.session.session_key

        order.save()

        user_carts = get_user_carts(self.request)
        for cart in user_carts:
            OrderItem.objects.create(
                order=order,
                product_variation=cart.product_variation,
                quantity=cart.quantity,
            )

        user_carts.delete()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = True
        return context
