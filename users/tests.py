from django.test import TestCase

from users.models import User


class UserTestCase(TestCase):

    def test_create_users(self):
        User.objects.create(email='abc@gmail.com', username='abc', password='123', first_name='z', last_name='x')
        User.objects.create(email='joshpeck@gmail.com', username='notdrake', password='hugmebr0tha', first_name='Josh', last_name='Peck')
        user_one = User.objects.get(username='abc')
        user_two = User.objects.get(username='notdrake')

        self.assertEqual(user_one.username, 'abc')
        self.assertEqual(user_two.last_login, None)
