from django.test import TestCase
# Create your tests here.
from django.utils import timezone

from catering.models import CaterRequest
from trucks.models import Truck
from users.models import User


class TestCatering(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(
            'onthegrub@gmail.com',
            'onthegrub',
            'XXX',
        )
        self.truck = Truck.objects.create(
            title='Truck name',
            owner=self.user
        )

        self.cater = CaterRequest.objects.create(
            truck=self.truck,
            name='onthegrub',
            email='onthegrub@gmail.com',
            phone='1-111-111-1111',
            details='Event details',
            when=timezone.now(),
            duration=1,
        )

    def test_status_changes(self):
        self.assertIs(self.cater.status, 'pending')
        self.cater.reject()
        self.assertIs(self.cater.status, 'rejected')
        self.cater.accept()
        self.assertIs(self.cater.status, 'accepted')
