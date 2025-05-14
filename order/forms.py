from django import forms

from order.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["user", "status", "created_at"]
