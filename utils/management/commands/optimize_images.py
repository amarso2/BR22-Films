from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import ImageField

from utils.image_optimizer import SUPPORTED_EXTENSIONS, optimize_image


class Command(BaseCommand):
    help = "Convert existing JPG, JPEG, and PNG uploads to WebP."

    def handle(self, *args, **options):
        converted = 0
        skipped = 0
        errors = 0

        for model in apps.get_models():
            image_fields = [
                field for field in model._meta.get_fields()
                if isinstance(field, ImageField)
            ]
            if not image_fields:
                continue

            for instance in model._default_manager.all().iterator():
                for field in image_fields:
                    image_field = getattr(instance, field.name, None)
                    if not image_field or not image_field.name:
                        skipped += 1
                        continue

                    if Path(image_field.name).suffix.lower() not in SUPPORTED_EXTENSIONS:
                        skipped += 1
                        continue

                    try:
                        optimized = optimize_image(image_field)
                        if optimized is None:
                            skipped += 1
                            continue

                        image_field.save(optimized.name, optimized, save=False)
                        instance.save(update_fields=[field.name])
                        converted += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Converted {model._meta.label}.{field.name}: {image_field.name}"
                            )
                        )
                    except Exception as error:
                        errors += 1
                        self.stderr.write(
                            self.style.ERROR(
                                f"Failed {model._meta.label}.{field.name} "
                                f"for object {instance.pk}: {error}"
                            )
                        )

        self.stdout.write(
            f"Image optimization complete. Converted: {converted}; "
            f"Skipped: {skipped}; Errors: {errors}."
        )
