from datetime import datetime

from rest_framework.test import APITestCase

# Create your tests here.
from events.models import Event
from users.models import User


class EventsTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='zach',
            password='xxxxxx',
            first_name='Zach',
            last_name='Broad',
        )

        event = Event.objects.create(
            title='null',
            description='null',
            address='null',
            phone_number='111-111-1111',
            start_time=datetime.now(),
            end_time=datetime.now(),
            organizer=self.user,
        )

    def test_im_going(self):
        # request = APIRequestFactory().get("")
        # im_going_view = EventViewSet.as_view({'POST': 'going'})
        # im_going_view(request=request)
        self.client.force_login(self.user)
        response = self.client.post('/api/events/1/going/', format='json')
        # print(response.)
        self.assertLess(response.status_code, 300)
