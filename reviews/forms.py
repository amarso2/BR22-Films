from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["event", "rating", "message", "image"]

        widgets = {
            "event": forms.Select(attrs={"class": "form-control"}),
            "rating": forms.Select(
                choices=[(1,"⭐"),(2,"⭐⭐"),(3,"⭐⭐⭐"),(4,"⭐⭐⭐⭐"),(5,"⭐⭐⭐⭐⭐")],
                attrs={"class":"form-control"}
            ),
            "message": forms.Textarea(attrs={
                "class":"form-control",
                "rows":4
            }),
        }