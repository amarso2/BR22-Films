from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Booking


@receiver(post_save, sender=Booking)
def payment_confirmation_email(sender, instance, created, **kwargs):

    # Sirf Paid hone par email bhejna
    if not created and instance.payment_status == "Paid":

        subject = "BR22 FILMS - Payment Confirmed"

        message = render_to_string(
            "payments/payment_confirmation_email.html",
            {
                "booking": instance,
            }
        )

        email = EmailMessage(
            subject,
            message,
            to=[instance.email]
        )

        email.content_subtype = "html"
        email.send(fail_silently=True)