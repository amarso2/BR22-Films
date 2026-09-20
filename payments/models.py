from django.db import models
from django.conf import settings
from django.utils import timezone


class Booking(models.Model):

    BOOKING_TYPE = [
        ("package", "Package"),
        ("service", "Service"),
    ]

    PAYMENT_METHOD = [
        ("online", "Online Payment"),
        ("offline", "Offline Payment"),
    ]

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Offline Pending", "Offline Pending"),
        ("Failed", "Failed"),
    ]

    # Booking ID (Auto Generate)
    booking_id = models.CharField(max_length=20, unique=True, blank=True)

    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE)
    selected_item = models.CharField(max_length=100)

    # Customer Details
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)

    # Event Details
    bride_name = models.CharField(max_length=100, blank=True)
    groom_name = models.CharField(max_length=100, blank=True)
    event_date = models.DateField()
    event_location = models.CharField(max_length=200)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    note = models.TextField(blank=True)

    # Price
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    advance_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Payment
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    confirmation_email_sent = models.BooleanField(default=False)

    payment_screenshot = models.ImageField(
    upload_to="payments/screenshots/",
    blank=True,
    null=True
    )

    razorpay_order_id = models.CharField(max_length=200, blank=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True)
    razorpay_signature = models.CharField(max_length=300, blank=True)

    # Login User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            year = timezone.now().year
            last_booking = Booking.objects.order_by("-id").first()

            if last_booking:
                number = last_booking.id + 1
            else:
                number = 1

            self.booking_id = f"BR22-{year}-{number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} | {self.full_name}"