from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import Customer


class CreateLoanTest(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            customer_id=102,
            first_name="Create Loan",
            last_name="Test Case",
            phone_number="1234567890",
            age=35,
            monthly_salary=70000,
            approved_limit=2500000,
            current_debt=0
        )

    def test_create_loan_approved(self):
        url = reverse('create-loan')
        payload = {
            "customer_id": self.customer.customer_id,
            "loan_amount": 500000,
            "interest_rate": 14,
            "tenure": 12
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['loan_approved'])

    def test_create_loan_rejected(self):
        url = reverse('create-loan')
        payload = {
            "customer_id": self.customer.customer_id,
            "loan_amount": 500000,
            "interest_rate": 5,
            "tenure": 12
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data['loan_approved'])
