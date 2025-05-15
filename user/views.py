from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from user.forms import UserLoginForm


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])

            if user:
                login(request, user)
                messages.success(
                    request, "Ви успішно увійшли до свого облікового запису"
                )
                return redirect("product:catalog")
    else:
        form = UserLoginForm()

    context = {"form": form}

    return render(request, "user/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Ви успішно вийшли з облікового запису")
    return redirect("product:catalog")
