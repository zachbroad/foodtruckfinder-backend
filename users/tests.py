from django.test import TestCase

from users.models import Account


class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(email="abc@gmail.com",username="abc",password="123",first_name="z",last_name="x")
        Account.objects.create(email="joshpeck@gmail.com",username="notdrake",password="hugmebr0tha",first_name="Josh",last_name="Peck")


    def test_account(self):
        acc_one = Account.objects.get(username='abc')
        acc_two = Account.objects.get(username='notdrake')
        self.assertEqual(acc_one.username, 'abc')