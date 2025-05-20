from django.urls import reverse_lazy
from django.views import generic

from cart.models import Cart
from order.forms import OrderCreateForm
from order.models import Order, OrderItem


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order/detail.html"


class OrderCreateView(generic.CreateView):
    model = Order
    template_name = "order/create.html"
    form_class = OrderCreateForm
    success_url = reverse_lazy("product:catalog")

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        if not form.cleaned_data["email"]:
            order.email = "Не вказано"
        order.save()

        user_carts = Cart.objects.filter(user=self.request.user)
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
