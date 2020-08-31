from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from account.models import Account


CREATE_ACCOUNT_URL = reverse('account:create')
CREATE_TOKEN_URL = reverse('account:token')
ME_URL = reverse('account:me')


def create_account(**params) -> Account:
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

    def test_create_token_with_valid_credentials(self):
        create_account(**self.valid_payload)
        resp = self.client.post(CREATE_TOKEN_URL, self.valid_payload)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('token', resp.data)

    def test_create_token_with_invalid_credentials(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['password'] = 'wrong-password'

        create_account(**self.valid_payload)
        resp = self.client.post(CREATE_TOKEN_URL, invalid_payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', resp.data)

    def test_retrieve_self_profile_unauthorized(self):
        resp = self.client.get(ME_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAccountApiTests(TestCase):

    def setUp(self):
        self.user = create_account(
            email='test@ablog.com',
            password='password',
            username='test user'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_self_profile_authorized(self):
        resp = self.client.get(ME_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, {
            'email': self.user.email,
            'username': self.user.username
        })

    def test_update_self_profile_update(self):
        payload = {'email': 'new@mail.com',
                   'username': 'new name',
                   'password': 'new pass'}

        resp = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.username, payload['username'])
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
