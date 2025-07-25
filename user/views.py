from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from order.models import Order, OrderItem
from user.forms import (UserAccountForm, UserLoginForm, UserPasswordChangeForm,
                        UserRegisterForm)
from user.utils import transfer_session_cart_to_user


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(identifier=cd["identifier"], password=cd["password"])

            transfer_session_cart_to_user(request, user)

            if user:
                login(request, user)
                messages.success(
                    request, _("Ви успішно увійшли до свого облікового запису")
                )
                return redirect("product:сategories")
    else:
        form = UserLoginForm()

    context = {"form": form}

    return render(request, "user/login.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, _("Ви успішно вийшли з облікового запису"))
    return redirect("product:сategories")


class UserRegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = "user/register.html"
    success_url = reverse_lazy("product:сategories")

    def form_valid(self, form):
        user = form.save(commit=False)
        phone_number = form.cleaned_data["phone_number"]
        user.phone_number = phone_number.replace(" ", "")
        user.save()
        self.object = user

        transfer_session_cart_to_user(self.request, self.object)

        login(self.request, self.object)
        messages.success(self.request, _("Ви успішно зареєструвались і увійшли в акаунт."))
        return redirect(self.get_success_url())


class UserAccountView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    template_name = "user/account.html"
    form_class = UserAccountForm
    success_url = reverse_lazy("user:account")
    success_message = _("Акаунт успішно змінено")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        user.phone_number = form.cleaned_data["phone_number"].replace(" ", "")
        user.save()
        return super().form_valid(form)


class UserOrders(LoginRequiredMixin, generic.ListView):
    template_name = "user/user_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        query = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch("items", queryset=OrderItem.objects.select_related("product_variation__product__currency")))


        orders = cache.get_or_set(f"orders_for_{self.request.user.email}",
                                 query, 300)
        return orders


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("user:account")
    template_name = "user/password_change_form.html"
    success_message = _("Пароль успішно змінено")
