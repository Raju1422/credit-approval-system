from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import Customer


class CheckEligibilityTest(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            customer_id=101,
            first_name="Test",
            last_name="Case",
            phone_number="1234567890",
            age=32,
            monthly_salary=60000,
            approved_limit=2160000,
            current_debt=0
        )

    def test_check_loan_eligibility_success(self):
        url = reverse('check-eligibility')
        payload = {
            "customer_id": self.customer.customer_id,
            "loan_amount": 200000,
            "interest_rate": 13,
            "tenure": 12
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("approval", response.data)
        self.assertIn("monthly_installment", response.data)
