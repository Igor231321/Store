from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "surname", "phone_number", "password1", "password2"]


class UserAccountForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "surname", "phone_number"]
