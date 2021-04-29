from django.test import TestCase

from trucks.models import Truck
from users.models import User
from util.models import Comment


class TestComments(TestCase):
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

    def test_comment_truck(self):
        comment = Comment.objects.create(
            object_id=self.truck.id,
            owner=self.user,
            content_object=self.truck,
            text='This is a test comment'
        )

        self.assertEqual(1, self.truck.comments.count())
