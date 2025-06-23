from django import forms

from order.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["user", "session_key", "status", "created_at"]
        widgets = {
            "phone_number": forms.TextInput(attrs={'class': 'input'}),
            "first_name": forms.TextInput(attrs={'class': 'input'}),
            "last_name": forms.TextInput(attrs={'class': 'input'}),
            "surname": forms.TextInput(attrs={'class': 'input'}),
            "email": forms.EmailInput(attrs={'class': 'input'}),
            "delivery_method": forms.RadioSelect(),
            "country": forms.TextInput(attrs={'class': 'input'}),
            "post_office": forms.TextInput(attrs={'class': 'input', }),
            "terminal": forms.TextInput(attrs={'class': 'input', }),
            "comment": forms.Textarea(attrs={'class': 'input',
                                             'rows': '5', 'cols': '5'})
        }

    def clean(self):
        cleaned_data = super().clean()

        delivery_method = cleaned_data.get("delivery_method")
        post_office = cleaned_data.get("post_office")
        terminal = cleaned_data.get("terminal")

        if delivery_method == 'PO' and not post_office:
            self.add_error("post_office", "Будь ласка, оберіть відділення")
        elif delivery_method == 'TR' and not terminal:
            self.add_error("terminal", 'Будь ласка, оберіть поштомат')
