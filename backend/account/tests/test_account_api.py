from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_ACCOUNT_URL = reverse('account:create')


def create_account(**params):
    return get_user_model().objects.create_user(**params)


class PublicAccountApiTestCase(TestCase):

    valid_payload = {
        'email': 'test@ablog.com',
        'password': 'password',
        'username': 'test user'
    }

    def setUp(self):
        self.client = APIClient()

    def create_valid_account_success(self):
        resp = self.client.post(CREATE_ACCOUNT_URL,
                                data=self.valid_payload)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.valid_payload['email'])
        self.assertTrue(user.check_password(self.valid_payload['password']))
        self.assertNotIn('password', resp)

    def test_create_existing_account(self):
        create_account(**self.valid_payload)

        resp = self.client.post(CREATE_ACCOUNT_URL, self.valid_payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            'email': 'test@ablog.com',
            'password': 'pw',
        }
        resp = self.client.post(CREATE_ACCOUNT_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        account_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(account_exists)
