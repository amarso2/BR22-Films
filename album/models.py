from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from utils.image_optimizer import WebPImageModelMixin
from utils.storage import media_storage

User = get_user_model()


def default_expiry():
    return timezone.now() + timedelta(days=60)


class Album(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    # Existing registered users
    allowed_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="shared_albums"
    )

    expires_at = models.DateTimeField(default=default_expiry)
    is_active = models.BooleanField(default=True)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def days_left(self):
        remaining = self.expires_at - timezone.now()
        return max(0, remaining.days)

    def __str__(self):
        return self.title


class AlbumPage(WebPImageModelMixin, models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="pages"
    )
    page_number = models.PositiveIntegerField()
    image = models.ImageField(upload_to="albums/", storage=media_storage)

    class Meta:
        ordering = ["page_number"]

    def __str__(self):
        return f"{self.album.title} - Page {self.page_number}"