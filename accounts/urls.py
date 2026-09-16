from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

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
        auth_views.PasswordResetView.as_view(
            template_name="accounts/forgot_password.html",
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