from django.test import TestCase
from .models import Account

from django.db import transaction
from django.db.utils import IntegrityError


class AccountTestCase(TestCase):

    def setUp(self) -> None:
        self.normal_user = Account.objects.create_user(
            username='normal_user',
            email='normal@mail.com',
            password='1234'
        )

    def test_instance(self):
        user = Account.objects.get(username='normal_user')
        assert user == self.normal_user

    def test_requiered_fields(self):
        with self.assertRaises(ValueError):
            with transaction.atomic():
                Account.objects.create_user(email=None, username='u1', password='123')
        with self.assertRaises(ValueError):
            with transaction.atomic():
                Account.objects.create_user(email='e@m.com', username='u1', password=None)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Account.objects.create_user(email='e@m.com', username=None, password='123')

    def test_unique_fields(self):
        with self.assertRaises(IntegrityError, msg='emails must be unique'):
            with transaction.atomic():
                Account.objects.create_user(email='normal@mail.com', username='u1', password='123')

        with self.assertRaises(IntegrityError, msg='usernames must be unique'):
            with transaction.atomic():
                Account.objects.create_user(email='e2@m.com', username='normal_user', password='123')
