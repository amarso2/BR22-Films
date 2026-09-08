import hashlib
from django import template

register = template.Library()

@register.filter
def gravatar_url(email, size=40):
    email = (email or "").strip().lower()
    hash = hashlib.md5(email.encode("utf-8")).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash}?s={size}&d=mp"