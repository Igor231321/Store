from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from order.models import Order
from user.forms import UserAccountForm, UserLoginForm, UserRegisterForm
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
                    request, "Ви успішно увійшли до свого облікового запису"
                )
                return redirect("product:сategories")
    else:
        form = UserLoginForm()

    context = {"form": form}

    return render(request, "user/login.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Ви успішно вийшли з облікового запису")
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
        messages.success(self.request, "Ви успішно зареєструвались і увійшли в акаунт.")
        return redirect(self.get_success_url())


class UserAccountView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    template_name = "user/account.html"
    form_class = UserAccountForm
    success_url = reverse_lazy("user:account")
    success_message = "Акаунт успішно змінено"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        user.phone_number = form.cleaned_data["phone_number"].replace(" ", "")
        user.save()
        return super().form_valid(form)

class UserOrders(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "user/user_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
