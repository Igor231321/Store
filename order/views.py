from django.urls import reverse_lazy
from django.views import generic

from order.forms import OrderCreateForm
from order.models import Order


class OrdersListView(generic.ListView):
    model = Order
    template_name = "order/orders.html"
    context_object_name = "orders"


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order/detail.html"


class OrderCreateView(generic.CreateView):
    model = Order
    template_name = "order/create.html"
    form_class = OrderCreateForm
    success_url = reverse_lazy("product:catalog")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
