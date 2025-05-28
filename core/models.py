from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Customer(models.Model):
    customer_id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    age = models.PositiveIntegerField()
    monthly_salary = models.PositiveIntegerField()
    approved_limit = models.PositiveIntegerField()
    current_debt = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.customer_id})"
    


class Loan(models.Model):
    loan_id = models.PositiveIntegerField(primary_key=True)  # Use Loan ID as PK
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.FloatField()
    tenure = models.PositiveIntegerField(help_text="Tenure in months")
    interest_rate = models.FloatField(help_text="Annual interest rate")
    monthly_installment = models.FloatField()
    emis_paid_on_time = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.loan_id} for Customer {self.customer.customer_id}"

