from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,Loan
from .serializers import CustomerSerializer,CheckLoanEligibilityRequestSerializer,CheckLoanEligibilityResponseSerializer
from .utils import corrected_interest_rate,calculate_emi,compute_credit_score
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


class CheckEligibilityView(APIView):
    def post(self,request):
        try:
            request_serializer = CheckLoanEligibilityRequestSerializer(data=request.data)
            if not request_serializer.is_valid():
                return Response({
                    'error': 'Invalid request data',
                    'details': request_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            validated_data = request_serializer.validated_data
            customer_id = validated_data['customer_id']
            loan_amount = validated_data['loan_amount']
            interest_rate = validated_data['interest_rate']
            tenure = validated_data['tenure']

            customer = Customer.objects.get(customer_id=customer_id)
            loans = Loan.objects.filter(customer=customer)

            credit_score = compute_credit_score(customer,loans)
            print(credit_score)
            approved = False

            if credit_score > 50 :
                approved = True
            elif 30 < credit_score <= 50 and interest_rate >= 12:
                approved = True
            elif 10 < credit_score <= 30 and interest_rate >= 16:
                approved = True

            corrected_interest = corrected_interest_rate(credit_score, interest_rate)

            monthly_emi = calculate_emi(loan_amount,corrected_interest,tenure)
            total_emis = sum(loan.monthly_installment for loan in loans)
            if total_emis > ( 0.5*customer.monthly_salary):
                approved = False

            response = {
                "customer_id": customer.customer_id,
                "approval": approved,
                "interest_rate": interest_rate,
                "corrected_interest_rate": corrected_interest,
                "tenure": tenure,
                "monthly_installment": monthly_emi
            }
            response_serializer = CheckLoanEligibilityResponseSerializer(data=response)
            if response_serializer.is_valid():
                return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Internal server error',
                    'details':response_serializer.errors,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=404)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)