import os
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colorphoto.settings")

import django
django.setup()

from services.models import Services_details
from portfolio.models import Portfolio

ROOT = Path(r"D:\BR22_MEDIA")

def fix_path(name):
    p = ROOT / name

    if p.exists():
        return name

    stem = p.with_suffix("")
    for ext in [".webp", ".png", ".jpg", ".jpeg"]:
        alt = stem.with_suffix(ext)
        if alt.exists():
            return alt.relative_to(ROOT).as_posix()

    return name

# Services Details
for obj in Services_details.objects.all():
    changed = False

    for field in ["image1", "image2", "image3"]:
        f = getattr(obj, field)
        if f and f.name:
            new = fix_path(f.name)
            if new != f.name:
                setattr(obj, field, new)
                changed = True
                print("Services_details:", obj.id, field, "->", new)

    if changed:
        obj.save()

# Portfolio
for obj in Portfolio.objects.all():
    changed = False

    for field in ["image1", "image2", "image3"]:
        f = getattr(obj, field, None)

        if f and f.name:
            new = fix_path(f.name)
            if new != f.name:
                setattr(obj, field, new)
                changed = True
                print("Portfolio:", obj.id, field, "->", new)

    if changed:
        obj.save()

print("Done.")