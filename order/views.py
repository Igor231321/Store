from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic

from cart.utils import get_user_carts
from order.forms import OrderCreateForm
from order.models import Country, Order, OrderItem, Warehouse


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = "order/detail.html"


class OrderCreateView(SuccessMessageMixin, generic.CreateView):
    model = Order
    template_name = "order/create.html"
    form_class = OrderCreateForm
    success_url = reverse_lazy("product:сategories")
    success_message = "Ваше замовлення успішно створено"

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial["first_name"] = self.request.user.first_name
            initial["last_name"] = self.request.user.last_name
            initial["surname"] = self.request.user.surname
            initial["email"] = self.request.user.email
            initial["phone_number"] = self.request.user.phone_number
        return initial

    def form_valid(self, form):
        order = form.save(commit=False)
        cd = form.cleaned_data

        delivery_method = cd.get("delivery_method")
        if delivery_method == "TR":
            order.terminal = cd.get("terminal")
        else:
            order.post_office = cd.get("post_office")

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
        context["selected_country_pk"] = self.request.POST.get("country_pk")
        context["selected_country_text"] = self.request.POST.get("country_text")
        return context


def get_countries(request):
    query = request.GET.get("query", "")
    country_types = {
        "місто": "м.",
        "село": "с.",
        "селище міського типу": "смт."
    }

    countries = Country.objects.filter(description__icontains=query)

    data = [{
        "id": c.id,
        "description": f"{country_types.get(c.country_type, '')} {c.description}",
        "area_description": f"{c.area_description} обл."
    } for c in countries]

    return JsonResponse(data, safe=False)


def get_warehouses(request):
    country_pk = request.GET.get("country_pk")
    country = Country.objects.get(pk=country_pk)
    warehouses_type = request.GET.get("warehouse_type")

    if warehouses_type == "terminals":
        warehouses = country.warehouses.filter(warehouse_type=Warehouse.WarehouseType.TERMINAL)
    else:
        warehouses = country.warehouses.exclude(warehouse_type=Warehouse.WarehouseType.TERMINAL)

    query = request.GET.get("query", "")

    if query:
        warehouses = warehouses.filter(description__icontains=query)

    data = [{"description": wr.description, "id": wr.id} for wr in warehouses]

    return JsonResponse({"data": data})
