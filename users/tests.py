from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User


class UserTests(TestCase):
    """Тесты для модели пользователя."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='user@example.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )

    def test_user_creation(self):
        """Тест создания пользователя."""
        self.assertEqual(self.user.email, 'user@example.com')
        self.assertTrue(self.user.check_password('test123'))

    def test_user_registration(self):
        """Тест регистрации через API."""
        url = reverse('users:register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
