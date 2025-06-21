from django import forms

from order.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["user", "session_key", "status", "created_at"]
