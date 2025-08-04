from django import forms
from django.utils.translation import gettext_lazy as _

from order.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["user", "session_key", "status", "created_at", "paid", "reference"]
        widgets = {
            "phone_number": forms.TextInput(attrs={'class': 'input'}),
            "first_name": forms.TextInput(attrs={'class': 'input'}),
            "last_name": forms.TextInput(attrs={'class': 'input'}),
            "surname": forms.TextInput(attrs={'class': 'input'}),
            "email": forms.EmailInput(attrs={'class': 'input'}),
            "delivery_method": forms.RadioSelect(),
            "np_country": forms.TextInput(attrs={'class': 'input'}),
            "np_warehouse": forms.TextInput(attrs={'class': 'input', }),
            "np_terminal": forms.TextInput(attrs={'class': 'input', }),

            "ukr_address": forms.TextInput(attrs={'class': 'input'}),
            "ukr_post_code": forms.NumberInput(attrs={'class': 'input'}),

            "meest_country": forms.TextInput(attrs={'class': "input"}),
            "meest_warehouse": forms.TextInput(attrs={'class': "input"}),
            "comment": forms.Textarea(attrs={'class': 'input',
                                             'rows': '5', 'cols': '5'})
        }

    def clean(self):
        cleaned_data = super().clean()

        delivery_method = cleaned_data.get("delivery_method")
        np_country = cleaned_data.get("np_country")
        np_warehouse = cleaned_data.get("np_warehouse")
        np_terminal = cleaned_data.get("np_terminal")

        ukr_address = cleaned_data.get("ukr_address")
        ukr_post_code = cleaned_data.get("ukr_post_code")

        meest_country = cleaned_data.get("meest_country")
        meest_warehouse = cleaned_data.get("meest_warehouse")

        if delivery_method in ["NP_WH", "NP_TR"] and not np_country:
            self.add_error("np_country", _("Будь ласка, оберіть населений пункт"))

        if delivery_method == 'NP_WH' and not np_warehouse:
            self.add_error("np_warehouse", _("Будь ласка, оберіть відділення"))
        elif delivery_method == 'NP_TR' and not np_terminal:
            self.add_error("np_terminal", _('Будь ласка, оберіть поштомат'))
        elif delivery_method == "UKR_WH":
            if not ukr_address:
                self.add_error("ukr_address", _('Будь ласка, введіть адресу Укрпошти'))
            if not ukr_post_code:
                self.add_error("ukr_post_code", _("Будь ласка, введіть поштовий індекс"))
        elif delivery_method == "MEEST_WH":
            if not meest_country:
                self.add_error("meest_country", _("Будь ласка, введіть ваше місто"))
            if not meest_warehouse:
                self.add_error("meest_warehouse", _("Будь ласка, введіть номер та адресу відділення"))
        return cleaned_data


class QuickOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number']

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
            "phone_number": forms.TextInput(attrs={"class": "input"})
        }
