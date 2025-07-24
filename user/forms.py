from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import (PasswordChangeForm, UserChangeForm,
                                       UserCreationForm)
from django.utils.translation import gettext_lazy as _

from user.services import normalize_phone_number


class UserLoginForm(forms.Form):
    identifier = forms.CharField(widget=forms.TextInput(attrs={"class": "input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input"}))

    def clean_identifier(self):
        data = self.cleaned_data["identifier"]

        if "@" in data:
            return data

        phone_number = normalize_phone_number(data)
        if not phone_number:
            raise forms.ValidationError(_("Невірний номер телефону"))

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


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Старий пароль"),
                                   widget=forms.PasswordInput(attrs={'class': "input"}))
    new_password1 = forms.CharField(label=_("Новий пароль"),
                                    widget=forms.PasswordInput(attrs={'class': "input"}))
    new_password2 = forms.CharField(label=_("Новий пароль (підтвердження)"),
                                    widget=forms.PasswordInput(attrs={'class': "input"}))
