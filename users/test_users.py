import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from courses.models import Course
from unittest.mock import patch

User = get_user_model()


class PaymentTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@example.com',
            password='pass'
        )
        cls.course = Course.objects.create(
            title='Test Course',
            description='Test',
            author=cls.user
        )

    def test_create_payment_success(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(
            '/api/payments/create/',
            {
                'course_id': self.course.id,
                'amount': 1990.00,
            },
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_payment_invalid_amount(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(
            '/api/payments/create/',
            {
                'course_id': self.course.id,
                'amount': -100,
            },
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'amount' in response.data






