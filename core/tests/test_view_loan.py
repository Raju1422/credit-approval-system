from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import Customer, Loan
from datetime import date, timedelta

class ViewLoanDetailTest(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            customer_id=103,
            first_name="View Loan",
            last_name="TestCase",
            phone_number="1234567890",
            age=40,
            monthly_salary=100000,
            approved_limit=3600000
        )
        self.loan = Loan.objects.create(
            loan_id=5001,
            customer=self.customer,
            loan_amount=200000,
            interest_rate=11.5,
            monthly_installment=17654.43,
            tenure=12,
            emis_paid_on_time=5,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365)
        )

    def test_view_loan(self):
        url = reverse('view-loan', kwargs={'loan_id': self.loan.loan_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['loan_id'], self.loan.loan_id)
        self.assertEqual(response.data['customer']['customer_id'], self.customer.customer_id)
