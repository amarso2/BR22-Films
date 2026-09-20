from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
import resend

from .models import Booking


@receiver(post_save, sender=Booking)
def payment_confirmation_email(sender, instance, created, **kwargs):
    if instance.payment_status != "Paid" or instance.confirmation_email_sent:
        return

    try:
        message = render_to_string(
            "payments/payment_confirmation_email.html",
            {
                "booking": instance,
                "user": instance.user,
                "amount": instance.advance_price,
                "event": instance.selected_item,
                "event_date": instance.event_date,
                "payment_id": instance.razorpay_payment_id,
            },
        )
        response = resend.Emails.send({
            "from": "BR22 FILMS <noreply@br22films.com>",
            "to": [instance.email],
            "subject": "Payment Confirmed – BR22 FILMS",
            "html": message,
        })
        print("PAYMENT EMAIL RESPONSE:", response)

        instance.confirmation_email_sent = True
        instance.save(update_fields=["confirmation_email_sent"])
    except Exception as e:
        print("PAYMENT EMAIL ERROR:", e)