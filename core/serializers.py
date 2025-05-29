from rest_framework import serializers
from .models import Customer, Loan


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


class CustomerLoanListSerializer(serializers.ModelSerializer):
    repayments_left = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            'loan_id',
            'loan_amount',
            'interest_rate',
            'monthly_installment',
            'repayments_left'
        ]

    def get_repayments_left(self, obj):
        return max(obj.tenure - obj.emis_paid_on_time, 0)
