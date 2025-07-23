from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.http import require_POST

from cart.utils import get_user_carts
from order.forms import OrderCreateForm, QuickOrderForm
from order.models import Country, Order, OrderItem, Warehouse
from product.models import ProductVariation


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = "order/detail.html"

    def get_object(self, queryset=None):
        order_id = self.kwargs["pk"]

        order = cache.get(f"order_{order_id}")
        if not order:
            order = Order.objects.get(id=order_id)
            cache.set(f"order_{order_id}", order, 60)
        return order


class OrderCreateView(SuccessMessageMixin, generic.CreateView):
    model = Order
    template_name = "order/create.html"
    form_class = OrderCreateForm
    success_url = reverse_lazy("product:сategories")
    success_message = _("Ваше замовлення успішно створено")

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

        order.np_country = None
        order.np_terminal = None
        order.np_warehouse = None
        order.ukr_address = None
        order.ukr_post_code = None
        order.meest_country = None
        order.meest_warehouse = None

        delivery_method = cd.get("delivery_method")
        if delivery_method == "NP_TR":
            order.np_country = cd.get("np_country")
            order.np_terminal = cd.get("np_terminal")
        elif delivery_method == "NP_WH":
            order.np_country = cd.get("np_country")
            order.np_warehouse = cd.get("np_warehouse")
        elif delivery_method == "UKR_WH":
            order.ukr_address = cd.get("ukr_address")
            order.ukr_post_code = cd.get("ukr_post_code")
        elif delivery_method == "MEEST_WH":
            order.meest_country = cd.get("meest_country")
            order.meest_warehouse = cd.get("meest_warehouse")

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


@require_POST
def quick_order_form(request):
    form = QuickOrderForm(request.POST)
    product_variation_id = request.POST.get("variation_id")
    product_variation = ProductVariation.objects.get(id=product_variation_id)
    quantity = request.POST.get("quantity")
    if form.is_valid():
        order = form.save()
        OrderItem.objects.create(
            order=order,
            product_variation=product_variation,
            quantity=quantity
        )
        messages.success(request, "Очікуйте дзвінка — ми з вами скоро зв'яжемося!")
        return redirect(request.META.get("HTTP_REFERER"))
    return QuickOrderForm
