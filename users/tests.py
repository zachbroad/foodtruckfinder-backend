from django.test import TestCase

from users.models import User


class AccountTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="abc@gmail.com", username="abc", password="123", first_name="z", last_name="x")
        User.objects.create(email="joshpeck@gmail.com", username="notdrake", password="hugmebr0tha", first_name="Josh", last_name="Peck")


    def test_account(self):
        acc_one = User.objects.get(username='abc')
        acc_two = User.objects.get(username='notdrake')
        self.assertEqual(acc_one.username, 'abc')