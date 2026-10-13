from django.test import TestCase
from django.urls import reverse

from .models import Bus, Seat


class BookingFlowTests(TestCase):
    def test_missing_seats_are_created_for_existing_bus(self):
        bus = Bus.objects.create(name='Express', source='Delhi', destination='Jaipur', price=800, total_seats=8)
        Seat.objects.filter(bus=bus).delete()

        response = self.client.get(f'/seat/{bus.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Seat.objects.filter(bus=bus).count(), 8)
        self.assertContains(response, 'Choose your seats')

    def test_passenger_form_posts_to_payment_flow(self):
        bus = Bus.objects.create(name='Express', source='Delhi', destination='Jaipur', price=800)
        session = self.client.session
        session['bus_id'] = bus.id
        session['seat_ids'] = ['1']
        session.save()

        response = self.client.get(reverse('passenger_page'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'action="{reverse("payment")}"')

    def test_bus_api_returns_json(self):
        Bus.objects.create(name='Express', source='Delhi', destination='Jaipur', price=800)

        response = self.client.get('/api/buses/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertGreater(len(response.json()), 0)
