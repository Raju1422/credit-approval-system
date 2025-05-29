from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class RegisterCustomerTest(APITestCase):
    def test_register_customer_success(self):
        url = reverse('register-customer')
        payload = {
            "first_name": "Test",
            "last_name": "Case",
            "age": 30,
            "monthly_income": 50000,
            "phone_number": "9999988888"
        }

        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["approved_limit"], 1800000)
   

    
