"""
Tests for the User API.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

TOKEN_URL = reverse('user:token')
USERS_URL = reverse('user:users')


class PublicUserApiTests(TestCase):
    """Test unauthenticated requests for user API."""

    def setUp(self) -> None:
        self.client = APIClient()
        return super().setUp()

    def test_authenticate_returns_token(self):
        """Test to authenticate succesful. returns token."""
        email = 'test@example.com'
        password = 'test123'
        get_user_model().objects.create_user(email, password)
        payload = {'email': email,
                   'password': password}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_error_bad_credentials(self):
        """Test to returns error if credentials invalid."""
        get_user_model().objects.create_user(email='test@example.com', password='goodpass', name='Test Name')
        payload = {'email': 'test@example.com', 'password': 'badpassword'}

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)


class PrivateUserApiTests(TestCase):
    """Test authenticated request for user API."""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def test_retrieve_list_of_users(self):
        """Test retrieve list of user successful."""
        get_user_model().objects.create_user(email='user2@example.com', password='test123')
        res = self.client.get(USERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
