from django import forms
from datetime import date
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            "phone",
            "bride_name",
            "groom_name",
            "event_date",
            "event_location",
            "city",
            "state",
            "note",
        ]

        widgets = {
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone Number"
            }),

            "bride_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Bride Name"
            }),

            "groom_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Groom Name"
            }),

            "event_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
                "min": date.today().isoformat(),
            }),

            "event_location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Event Venue"
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City"
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "State"
            }),

            "note": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Any special requirement (optional)"
            }),
        }

    def clean_payment_screenshot(self):
        screenshot = self.cleaned_data.get("payment_screenshot")

        if not screenshot:
            raise forms.ValidationError("Please upload your payment screenshot.")

        return screenshot


class OfflinePaymentForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["payment_screenshot"]

        widgets = {
            "payment_screenshot": forms.FileInput(attrs={
                "class": "form-control-file",
                "accept": "image/*"
            })
        }