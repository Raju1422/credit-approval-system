from rest_framework import serializers
from .models import Customer,Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'customer_id',
            'first_name',
            'last_name',
            'age',
            'monthly_salary',
            'approved_limit',
            'phone_number'
        ]
        read_only_fields = ['customer_id']

class CheckLoanEligibilityRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()


class CheckLoanEligibilityResponseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    approval = serializers.BooleanField()
    interest_rate = serializers.FloatField()
    corrected_interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()
    monthly_installment = serializers.FloatField()


class CreateLoanResponseSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField(allow_null=True)
    customer_id = serializers.IntegerField()
    loan_approved = serializers.BooleanField()
    message = serializers.CharField()
    monthly_installment = serializers.FloatField(allow_null=True)

class LoanDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Loan
        fields = [
            'loan_id',
            'customer',
            'loan_amount',
            'interest_rate',
            'monthly_installment',
            'tenure'
        ]


