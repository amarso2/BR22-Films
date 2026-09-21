from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def optimize_image(image_field, quality=80):
    """Return a WebP ContentFile for a supported Django ImageField value."""
    if not image_field or not image_field.name:
        return None

    if not image_field.storage.exists(image_field.name):
        return None

    suffix = Path(image_field.name).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        return None

    with Image.open(image_field.file) as image:
        if "A" in image.getbands() or image.mode in ("RGBA", "LA", "P"):
            converted = image.convert("RGBA")
        else:
            converted = image.convert("RGB")

        output = BytesIO()
        converted.save(output, format="WEBP", quality=quality, method=6)

    content = ContentFile(output.getvalue())
    content.name = f"{Path(image_field.name).with_suffix('').name}.webp"
    return content


class WebPImageModelMixin:
    """Convert supported ImageField uploads before a model is saved."""

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if not hasattr(field, "upload_to"):
                continue

            image_field = getattr(self, field.name, None)
            optimized = optimize_image(image_field)
            if optimized is not None:
                image_field.save(optimized.name, optimized, save=False)

        return super().save(*args, **kwargs)
