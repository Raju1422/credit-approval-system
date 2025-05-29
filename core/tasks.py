from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import timedelta, date


@shared_task
def ingest_customer_data(file_path):
    try:
        df = pd.read_excel(file_path)
        customers_to_create = []
        batch_size = 50

        for _, row in df.iterrows():
            customer = Customer(
                customer_id=row['Customer ID'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=row['Age'],
                phone_number=str(row['Phone Number']),
                monthly_salary=row['Monthly Salary'],
                approved_limit=row['Approved Limit'],
                current_debt=0,  # default
            )
            customers_to_create.append(customer)
            if len(customers_to_create) >= batch_size:
                Customer.objects.bulk_create(customers_to_create, batch_size=batch_size)
                customers_to_create.clear()
        if customers_to_create:
            Customer.objects.bulk_create(customers_to_create, batch_size=batch_size)
        return f"{len(df)} customers ingested successfully."

    except Exception as e:
        return f"Error during import: {str(e)}"


@shared_task
def ingest_loan_data(file_path):
    try:
        df = pd.read_excel(file_path)
        loans_to_create = []
        seen_loan_ids = set()
        batch_size = 50

        for _, row in df.iterrows():
            customer_id = row['Customer ID']
            loan_id = row['Loan ID']

            if loan_id in seen_loan_ids:
                print(f"Loan {loan_id} duplicated in file. Skipping.")
                continue
            seen_loan_ids.add(loan_id)

            try:
                customer = Customer.objects.get(customer_id=customer_id)
            except Customer.DoesNotExist:
                print("customer does not exist")
                continue

            if Loan.objects.filter(loan_id=loan_id).exists():
                print(f"Loan {loan_id} already exists. Skipping.")
                continue

            start_date = pd.to_datetime(row.get('Date of Approval')).date()
            end_date = pd.to_datetime(row.get('End Date')).date()
            loan = Loan(
                loan_id=loan_id,
                customer=customer,
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_installment=row['Monthly payment'],
                emis_paid_on_time=row['EMIs paid on Time'],
                start_date=start_date,
                end_date=end_date,
            )
            loans_to_create.append(loan)

            if len(loans_to_create) >= batch_size:
                Loan.objects.bulk_create(loans_to_create, batch_size=batch_size)
                loans_to_create.clear()

        if loans_to_create:
            Loan.objects.bulk_create(loans_to_create, batch_size=batch_size)

        return f"{len(df)} loans ingested successfully."
    except Exception as e:
        return f"Error during import: {str(e)}"
