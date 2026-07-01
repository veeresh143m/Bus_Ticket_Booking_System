from django.test import TestCase
from django.urls import reverse

from .models import Bus


class BookingFlowTests(TestCase):
    def test_passenger_form_posts_to_payment_flow(self):
        bus = Bus.objects.create(name='Express', source='Delhi', destination='Jaipur', price=800)
        session = self.client.session
        session['bus_id'] = bus.id
        session['seat_ids'] = ['1']
        session.save()

        response = self.client.get(reverse('passenger_page'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'action="{reverse("payment")}"')
