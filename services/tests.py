from django.test import TestCase
from django.urls import reverse

from services.models import Services, Services_details


class ServicesDetailViewTests(TestCase):
    def test_service_detail_renders_service_detail_data(self):
        service = Services.objects.create(
            service_name='Wedding Coverage',
            description='Classic wedding film package',
            price1=19999,
            price2=24999,
            stock=True,
            is_available=True,
        )
        Services_details.objects.create(
            id=service.id,
            title='Wedding Coverage',
            image1='photos/services_details/sample.jpg',
            about='Our cinematic coverage.',
            cover='Luxury wedding stories.',
            photographer='Raj',
            videographer='Amit',
            drone='Drone shots included',
            Deliverables='200 photos + highlight film',
        )

        response = self.client.get(reverse('service_detail', args=[service.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wedding Coverage')
        self.assertContains(response, 'Raj')
