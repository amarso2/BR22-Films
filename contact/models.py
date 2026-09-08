from django.db import models
from django.core.validators import RegexValidator


class Contact(models.Model):

    class Event(models.TextChoices):
        WEDDING = "Wedding", "Wedding"
        ENGAGEMENT = "Engagement", "Engagement"
        BIRTHDAY = "Birthday", "Birthday"
        MATERNITY = "Maternity", "Maternity"
        BABY_SHOOT = "Baby Shoot", "Baby Shoot"
        JANUE = "Janue", "Janue"
        CORPORATE = "Corporate Event", "Corporate Event"
        PRODUCT = "Product Photography", "Product Photography"

    name = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Enter a valid 10-digit phone number."
            )
        ]
    )

    email = models.EmailField(max_length=100)
    city = models.CharField(max_length=100)

    event = models.CharField(
        max_length=30,
        choices=Event.choices,
        default=Event.WEDDING
    )

    event_date = models.DateField()

    message = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event}"