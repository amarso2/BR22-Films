from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from .models import Account


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            first_name="Test",
            last_name="User",
            username="testuser",
            email="test@example.com",
            password="correct-password",
        )

    def test_login_with_correct_credentials_redirects_home(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"email": self.user.email, "password": "correct-password"},
        )

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(self.client.session["_auth_user_id"], str(self.user.pk))

    def test_login_with_incorrect_credentials_returns_to_login(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"email": self.user.email, "password": "wrong-password"},
            follow=True,
        )

        self.assertRedirects(response, reverse("accounts:login"))
        self.assertContains(response, "Invalid email or password.")

    def test_logged_in_user_can_logout_and_redirect_to_login(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts:logout"), follow=True)

        self.assertRedirects(response, reverse("accounts:login"))
        self.assertNotIn("_auth_user_id", self.client.session)