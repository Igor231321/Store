import time

import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from cart.utils import get_user_carts
from integrations.services.wayforpay_services import generate_signature
from order.forms import OrderCreateForm, QuickOrderForm
from order.models import Country, Order, OrderItem, Warehouse
from order.services import generate_reference
from product.models import ProductVariation


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = "order/detail.html"

    def get_object(self, queryset=None):
        order_id = self.kwargs["pk"]

        order = cache.get(f"order_{order_id}")
        if not order:
            order = Order.objects.prefetch_related(
                Prefetch("items",
                         queryset=OrderItem.objects.select_related("product_variation__product",
                                                                   "product_variation__attribute_value",
                                                                   "product_variation__attribute_value__attribute"))
            ).get(id=order_id)
            cache.set(f"order_{order_id}", order, 60)
        return order


class OrderCreateView(generic.CreateView):
    model = Order
    template_name = "order/create.html"
    form_class = OrderCreateForm
    success_url = reverse_lazy("product:categories")

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
        order.reference = generate_reference()

        order.save()

        user_carts = get_user_carts(self.request)
        products_name = []
        products_price = []
        products_count = []
        for cart in user_carts:
            products_name.append(str(cart.product_variation))
            products_price.append(cart.product_variation.get_price_with_discount())
            products_count.append(cart.quantity)

        order_data = {
            "transactionType": "CREATE_INVOICE",
            "merchantAccount": "test_merch_n1",
            "merchantAuthType": "SimpleSignature",
            "merchantDomainName": "127.0.0.1",
            "orderReference": f"{order.reference}",
            "apiVersion": 1,
            "orderDate": int(time.time()),
            "clientFirstName": order.first_name,
            "clientLastName": order.last_name,
            "clientPhone": order.phone_number,
            "clientEmail": order.email if order.email else "",
            "productName": products_name,
            "productPrice": list(map(str, products_price)),
            "productCount": list(map(str, products_count)),
            "amount": str(user_carts.total_sum()),
            "currency": "UAH",
            "serviceUrl": "https://25d911808be1.ngrok-free.app//uk/integrations/wayforpay_callback/",
            "approvedUrl": "https://25d911808be1.ngrok-free.app//uk/order/thanks_order/",
        }

        order_data["merchantSignature"] = generate_signature(order_data)

        res = requests.post("https://api.wayforpay.com/api", json=order_data).json()
        if res["reason"] == "Ok":
            return redirect(res["invoiceUrl"])
        else:
            print(res)

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


@csrf_exempt
def thanks_order(request):
    order_reference = request.POST["orderReference"]

    order = cache.get(f"order-{order_reference}")
    if not order:
        order = Order.objects.prefetch_related(
            Prefetch("items", queryset=OrderItem.objects.select_related("product_variation__product",
                                                                        "product_variation__attribute_value__attribute",
                                                                        "product_variation__attribute_value"))
        ).get(reference=order_reference)
        cache.set(f"order-{order_reference}", order, 600)

    return render(request, "order/detail.html", {"order": order, "info": True})
