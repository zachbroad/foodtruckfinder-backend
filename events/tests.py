from datetime import datetime

from rest_framework.test import APITestCase

# Create your tests here.
from events.models import Event, ImGoing
from users.models import User


class EventsTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='zach',
            password='xxxxxx',
            first_name='Zach',
            last_name='Broad',
        )

        self.event = Event.objects.create(
            title='null',
            description='null',
            address='null',
            phone_number='111-111-1111',
            start_time=datetime.now(),
            end_time=datetime.now(),
            organizer=self.user,
        )

    def test_im_going(self):
        self.client.force_login(self.user)

        # Say that I'm going
        response = self.client.post('/api/events/1/going/', format='json')
        self.assertLess(response.status_code, 300)

        # Check that GET shows that I am attending correctly
        response = self.client.get('/api/events/1/going/', format='json')
        self.assertTrue(response.data['going'])

        # Delete my intent to attend event
        response = self.client.delete('/api/events/1/going/', format='json')
        self.assertLess(response.status_code, 300)

        # Check that GET shows I am not attending correctly
        response = self.client.get('/api/events/1/going/', format='json')
        self.assertFalse(response.data['going'])

    def test_im_not_going(self):
        self.client.force_login(self.user)

        # Check that GET shows I am not attending correctly
        response = self.client.get('/api/events/1/going/', format='json')
        self.assertFalse(response.data['going'])

        # I'm going...
        response = self.client.post('/api/events/1/going/', format='json')
        self.assertLess(response.status_code, 300)
        self.assertIsNotNone(ImGoing.objects.filter(event=self.event, user=self.user).first())

        # Not going anymore
        response = self.client.delete('/api/events/1/going/', format='json')
        self.assertLess(response.status_code, 300)
        self.assertIsNone(ImGoing.objects.filter(event=self.event, user=self.user).first())
