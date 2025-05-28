from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,Loan
from .serializers import CustomerSerializer
# Create your views here.

class CustomerRegisterView(APIView):
    def post(self,request):
        try:
            data = request.data.copy()
            salary = int(data['monthly_income'])  # Cast to integer
            data['monthly_salary'] = salary
            data['approved_limit'] = round(36 * salary, -5)
            serializer = CustomerSerializer(data=data)
            if serializer.is_valid():
                customer = serializer.save()
                response_data = {
                    "customer_id": customer.customer_id,
                    "name": f"{customer.first_name} {customer.last_name}",
                    "age": customer.age,
                    "monthly_income": customer.monthly_salary,
                    "approved_limit": customer.approved_limit,
                    "phone_number": customer.phone_number
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Monthly income/salary must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

