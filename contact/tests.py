from django.test import TestCase
from django.urls import reverse


class HomeContactContextTests(TestCase):
    def test_home_has_contact_form_context(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('events', response.context)
        self.assertIn('today', response.context)

    def test_submit_contact_redirects_to_home_contact_section(self):
        response = self.client.post(
            reverse('contact'),
            {
                'name': 'Test User',
                'phone': '9876543210',
                'email': 'test@example.com',
                'city': 'Bettiah',
                'event': 'Wedding',
                'event_date': '2026-09-15',
                'message': 'Need booking details',
            },
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('home'))
