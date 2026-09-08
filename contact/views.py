from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from datetime import date



def submit_contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            city=request.POST.get("city"),
            event=request.POST.get("event"),
            event_date=request.POST.get("event_date"),
            message=request.POST.get("message")
        )

        messages.success(request, "Your booking request has been submitted successfully!")
        return redirect("contact")

    return render(request, "contact/contact.html", {
        "events": Contact.Event.choices, 
        "today": date.today(),
    })