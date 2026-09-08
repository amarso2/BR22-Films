import logging

from django.contrib import messages
from django.shortcuts import render


logger = logging.getLogger(__name__)


def dummy_admin(request):
    if request.method == "POST":
        logger.warning(
            "Dummy admin login attempt from %s using username %r",
            request.META.get("REMOTE_ADDR", "unknown"),
            request.POST.get("username", ""),
        )
        messages.error(request, "Invalid username or password.")

    return render(request, "honeypot/admin_login.html")
