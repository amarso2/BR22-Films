from decimal import Decimal

import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import resend

from package.models import Package, Package_details
from services.models import Services

from .forms import BookingForm, OfflinePaymentForm
from .models import Booking

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


@login_required
def booking_page(request, booking_type, item_id):

    package_details = None

    # Package ya Service fetch karo
    if booking_type == "package":
        item = get_object_or_404(Package, id=item_id)

        title = item.title
        description = "Complete Package Booking"

        # Total Price
        price = item.price1

        # Advance Base Price (price2)
        price2 = item.price2 if item.price2 else item.price1

        # Package details (image, about, etc.)
        package_details = Package_details.objects.filter(title1=item.title).first()

    elif booking_type == "service":
        item = get_object_or_404(Services, id=item_id)

        title = item.service_name
        description = item.description

        # Total Price
        price = item.price1

        # Advance Base Price (price2)
        price2 = item.price2 if item.price2 else item.price1

    else:
        return redirect("home")

    # 30% of price2
    advance = (price2 * Decimal("0.30")).quantize(Decimal("0.01"))

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            booking.user = request.user
            booking.booking_type = booking_type
            booking.selected_item = title

            # Auto-fill from profile
            booking.full_name = f"{request.user.first_name} {request.user.last_name}"
            booking.email = request.user.email

            # Save prices
            booking.total_price = price
            booking.advance_price = advance

            booking.save()

            # Next step me payment page par redirect karenge
            return redirect("payment_method", booking.booking_id)

    else:
        form = BookingForm(initial={
            "phone": request.user.phone_number
        })

    context = {
        "form": form,
        "booking_type": booking_type,
        "item": item,
        "package_details": package_details,
        "title": title,
        "description": description,
        "price": price,
        "price2": price2,
        "advance": advance,
    }

    return render(request, "payments/booking.html", context)

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def payment_method(request, booking_id):

    booking = get_object_or_404(
        Booking,
        booking_id=booking_id,
        user=request.user
    )

    if booking.payment_status == "Paid":
        return redirect("payment_success", booking.booking_id)

    if not booking.razorpay_order_id:
        order = client.order.create({
            "amount": int(booking.advance_price * 100),
            "currency": "INR",
            "receipt": booking.booking_id,
            "notes": {
                "booking_id": booking.booking_id,
            },
        })

        booking.razorpay_order_id = order["id"]
        booking.save(update_fields=["razorpay_order_id"])

    callback_url = request.build_absolute_uri(
        reverse("payment_success", args=[booking.booking_id])
    )

    return render(
        request,
        "payments/payment_method.html",
        {
            "booking": booking,
            "key": settings.RAZORPAY_KEY_ID,
            "amount_paise": int(booking.advance_price * 100),
            "callback_url": callback_url,
        }
    )


@login_required
def offline_payment(request, booking_id):

    booking = get_object_or_404(
        Booking,
        booking_id=booking_id,
        user=request.user
    )

    if request.method == "POST":

        form = OfflinePaymentForm(
            request.POST,
            request.FILES,
            instance=booking
        )

        if form.is_valid():
            booking = form.save(commit=False)

            booking.payment_status = "Offline Pending"
            booking.payment_method = "offline"
            booking.save()

            return redirect("offline_success", booking.booking_id)

    else:
        form = OfflinePaymentForm(instance=booking)

    return render(
        request,
        "payments/offline_payment.html",
        {
            "booking": booking,
            "form": form
        }
    )

@login_required
def offline_success(request, booking_id):

    booking = get_object_or_404(
        Booking,
        booking_id=booking_id,
        user=request.user
    )

    return render(
        request,
        "payments/offline_success.html",
        {"booking": booking}
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def payment_success(request, booking_id):
    booking = get_object_or_404(
        Booking,
        booking_id=booking_id
    )

    if request.method == "GET":
        if booking.payment_status == "Paid":
            return render(request, "payments/payment_success.html", {
                "booking": booking
            })
        return redirect("payment_method", booking.booking_id)

    payment_id = request.POST.get("razorpay_payment_id")
    order_id = request.POST.get("razorpay_order_id")
    signature = request.POST.get("razorpay_signature")

    if not all((payment_id, order_id, signature)):
        messages.error(request, "Payment verification details are missing.")
        return redirect("payment_method", booking.booking_id)

    if order_id != booking.razorpay_order_id:
        messages.error(request, "Payment order does not match this booking.")
        return redirect("payment_method", booking.booking_id)

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })
    except razorpay.errors.SignatureVerificationError:
        messages.error(request, "Payment verification failed. Your booking is still pending.")
        return redirect("payment_method", booking.booking_id)
    except (KeyError, ValueError, TypeError):
        messages.error(request, "Payment verification could not be completed.")
        return redirect("payment_method", booking.booking_id)

    booking.razorpay_order_id = order_id
    booking.razorpay_payment_id = payment_id
    booking.razorpay_signature = signature
    booking.payment_method = "online"
    booking.payment_status = "Paid"
    booking.save(update_fields=[
        "razorpay_order_id",
        "razorpay_payment_id",
        "razorpay_signature",
        "payment_method",
        "payment_status",
    ])

    try:
        message = render_to_string(
            "payments/payment_confirmation_email.html",
            {
                "booking": booking,
                "user": booking.user,
                "amount": booking.advance_price,
                "event": booking.selected_item,
                "event_date": booking.event_date,
                "payment_id": booking.razorpay_payment_id,
            },
        )
        response = resend.Emails.send({
            "from": "BR22 FILMS <noreply@br22films.com>",
            "to": [booking.email],
            "subject": "Payment Confirmed – BR22 FILMS",
            "html": message,
        })
        print("PAYMENT EMAIL RESPONSE:", response)
    except Exception as e:
        print("PAYMENT EMAIL ERROR:", e)

    return render(request, "payments/payment_success.html", {
        "booking": booking
    })
