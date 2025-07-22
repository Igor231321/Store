from django import forms

from product.models import Review


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
