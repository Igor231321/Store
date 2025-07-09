from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext as _

from user.services import normalize_phone_number


class UserLoginForm(forms.Form):
    identifier = forms.CharField(widget=forms.TextInput(attrs={"class": "input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input"}))

    def clean_identifier(self):
        data = self.cleaned_data["identifier"]

        # Если email (содержит @) — возвращаем как есть
        if "@" in data:
            return data

        # Иначе — пробуем нормализовать как номер
        phone_number = normalize_phone_number(data)
        if not phone_number:
            raise forms.ValidationError("Невірний номер телефону")

        return phone_number

    def clean(self):
        cd = super().clean()

        identifier = cd["identifier"]
        password = cd["password"]

        if identifier and password:
            user = authenticate(identifier=identifier, password=password)

            if not user:
                raise forms.ValidationError(_("Користувача з такими даними не знайдено або пароль невірний."))

        return cd


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "surname", "phone_number", "password1", "password2"]


class UserAccountForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "surname", "phone_number"]
