from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
import traceback
from .models import Account, PasswordResetToken
from .models import Account, PasswordResetToken
from .forms import RegistrationForm, EditProfileForm
from .tokens import account_activation_token
from payments.models import Booking

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            phone_number= form.cleaned_data['phone_number']
            email = form.cleaned_data["email"]
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.is_active = False  # Deactivate account until it is confirmed
            
            user.save()

            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'domain': settings.PASSWORD_RESET_DOMAIN,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_message = EmailMessage(
                "Verify your BR 22 FILMS account",
                message,
                to=[email],
            )
            email_message.content_subtype = "html"
            try:
                email_message.send(fail_silently=False)
            except Exception as error:
                traceback.print_exc()
                messages.error(
                    request,
                    f"Your account was created, but the verification email could not be sent: {error}",
                )
                return redirect("accounts:login")

            messages.success(request, "Registration successful. Please check your email to verify your account.")
            return redirect("accounts:login")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")

        messages.error(request, "Invalid email/password or please verify your email and password.")
        return redirect("accounts:login")
    return render(request, "accounts/login.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        messages.success(request, "Email verified successfully.")
        return redirect("home")

    messages.error(request, "Verification link is invalid or expired.")
    return redirect("accounts:login")

@login_required
def profile(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by("-created_at")

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = EditProfileForm(instance=user)

    return render(request, "accounts/profile.html", {
        "form": form,
        "bookings": bookings,
    })
    
@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = Account.objects.get(email=email)

            # Old unused tokens delete
            PasswordResetToken.objects.filter(user=user, is_used=False).delete()

            # Create new token (1 hour expiry)
            reset_token = PasswordResetToken.objects.create(
                user=user,
                expires_at=timezone.now() + timedelta(hours=1)
            )

            current_site = get_current_site(request)

            reset_link = request.build_absolute_uri(
                reverse("reset_password", args=[str(reset_token.token)])
            )

            message = render_to_string("accounts/reset_password_email.html", {
                "user": user,
                "reset_link": reset_link,
                "expiry": "1 hour",
                "domain": current_site.domain,
            })

            email_message = EmailMessage(
                "Reset your BR22 FILMS password",
                message,
                to=[email],
            )
            email_message.content_subtype = "html"
            email_message.send()

            messages.success(request, "Password reset link has been sent to your email.")

        except Account.DoesNotExist:
            messages.error(request, "No account found with this email.")

        return redirect("forgot_password")

    return render(request, "accounts/forgot_password.html")


def reset_password(request, token):
    try:
        reset = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Invalid reset link.")
        return redirect("accounts:login")

    if not reset.is_valid():
        messages.error(request, "This reset link has expired.")
        return redirect("forgot_password")

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password", token=token)

        reset.user.set_password(password1)
        reset.user.save()

        reset.is_used = True
        reset.save()

        messages.success(request, "Password changed successfully.")
        return redirect("accounts:login")

    return render(request, "accounts/reset_password.html", {"token": token})
