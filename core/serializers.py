from rest_framework import serializers
from .models import Customer

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