from django.db import models
from django.conf import settings
from utils.image_optimizer import WebPImageModelMixin

class Review(WebPImageModelMixin, models.Model):

    EVENT_CHOICES = [
        ("Wedding","Wedding"),
        ("Pre Wedding","Pre Wedding"),
        ("Birthday","Birthday"),
        ("Engagement","Engagement"),
        ("Maternity","Maternity"),
        ("Corporate","Corporate"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    event = models.CharField(max_length=30, choices=EVENT_CHOICES)

    rating = models.IntegerField(default=5)

    message = models.TextField()

    image = models.ImageField(
        upload_to="review_images/",
        blank=True,
        null=True
    )

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.rating}⭐"