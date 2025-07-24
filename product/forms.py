from django import forms

from product.models import InStockNotification, Review


class UploadDataForm(forms.Form):
    csv_file = forms.FileField()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["comment", "first_name", "last_name", "advantages", "disadvantages"]
        widgets = {
            "comment": forms.TextInput(attrs={"class": "input"}),
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
            "advantages": forms.TextInput(attrs={"class": "input"}),
            "disadvantages": forms.TextInput(attrs={"class": "input"})
        }


class InStockNotificationForm(forms.ModelForm):
    class Meta:
        model = InStockNotification
        fields = ["first_name", "last_name", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "input"}
            )
