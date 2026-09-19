from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.http import HttpResponseRedirect
from django.template import loader
import resend
from . import views

class ProjectPasswordResetForm(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = loader.render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        html_email = loader.render_to_string(html_email_template_name, context)

        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [to_email],
            "subject": subject,
            "text": body,
            "html": html_email,
        })


class PublicPasswordResetView(auth_views.PasswordResetView):
    def form_valid(self, form):
        opts = {
            "use_https": settings.PASSWORD_RESET_PROTOCOL == "https",
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
        }
        try:
            form.save(domain_override=settings.PASSWORD_RESET_DOMAIN, **opts)
        except Exception as error:
            import traceback

            traceback.print_exc()
            from django.contrib import messages

            messages.error(
                self.request,
                f"The password reset email could not be sent: {error}",
            )
            return HttpResponseRedirect(self.request.path)
        return HttpResponseRedirect(self.get_success_url())

app_name = "accounts"

urlpatterns = [
    # Account
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),

    # Forgot Password
    path(
        "forgot-password/",
        PublicPasswordResetView.as_view(
            template_name="accounts/forgot_password.html",
            form_class=ProjectPasswordResetForm,
            email_template_name="accounts/password_reset_email.txt",
            html_email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="forgot_password",
    ),

    # Reset Link Sent
    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    # Reset Password
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/reset_password.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),

    # Password Reset Complete
    path(
        "reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]