from django.test import TestCase
from django.urls import reverse

from package.models import Package, Package_details


class PackageDetailViewTests(TestCase):
    def test_package_detail_page_renders_package_data(self):
        package = Package.objects.create(
            title='Royal Wedding Package',
            price1=19999,
            price2=24999,
            t1='Photography',
            t2='Videography',
        )
        Package_details.objects.create(
            title1='Royal Wedding Package',
            image1='photos/package_details/sample.jpg',
            about='Our premium wedding package.',
            cover='Bride & groom preparation\nCandid moments',
            photographer='Photography team',
            videographer='Cinematic film team',
            drone='Drone coverage included',
            Deliverables='Album + highlight film',
        )

        response = self.client.get(reverse('package_details', args=[package.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Royal Wedding Package')
        self.assertContains(response, 'What We Cover')
        self.assertContains(response, 'Drone')
