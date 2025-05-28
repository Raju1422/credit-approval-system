from datetime import datetime
from django.db.models import Sum
def corrected_interest_rate(credit_score,interest_rate):
    """
    Determine corrected interest rate based on credit score
    """
    if credit_score > 50:
        return interest_rate
    if 30 < credit_score <= 50:
        return max(interest_rate, 12)
    if 10 < credit_score <= 30:
        return max(interest_rate, 16)
    return interest_rate

def calculate_emi(principal,annual_rate,tenure):
    """
    Calculate EMI using compound interest formula
    EMI = P * r * (1+r)^n / ((1+r)^n - 1)
    """

    #converting annual_rate to monthly_rate 
    monthly_rate = annual_rate/(12*100)

    if monthly_rate == 0:
        return round(principal / tenure, 2)
    
    emi = principal*monthly_rate*((1+monthly_rate)**tenure)/((1+monthly_rate)**tenure - 1)

    return round(emi,2)

def compute_credit_score(customer,loans):
    if customer.current_debt > customer.approved_limit:
        return 0

    credit_score = 0
    if loans.exists():
        # i. Past loans paid on time
        loans_paid_on_time_score = calculate_loans_paid_on_time(loans)
        # ii. No. of loans taken
        loan_frequency_score = calculate_loan_frequency_score(loans)
                
        # iii. Loan activity in current year 
        current_year_loan_activity_score = calculate_current_loan_activity(loans)

        # iv. Loan approved volume
        loan_approved_score = calculate_loan_approved_volume(customer,loans)

        credit_score = (
                loans_paid_on_time_score * 0.40 +  
                loan_frequency_score * 0.25 +   
                current_year_loan_activity_score * 0.20 +  
                loan_approved_score * 0.15        
            )
    else:
        credit_score = 50 
    
    return round(credit_score,2)



def calculate_loan_frequency_score(loans):
    """
    Too many loans = higher risk, too few = insufficient credit history
    """
    loan_count = loans.count()
        
    if loan_count == 0:
        return 80
    elif loan_count <= 2:
        return 70  
    elif loan_count <= 4:
        return 60  
    elif loan_count <= 6:
        return 50  
    elif loan_count <= 10:
        return 30  
    else:
        return 10  
    
def calculate_current_loan_activity(loans):
    """
    Calculate score based on current year loan activity
    """
    current_year = datetime.now().year
    current_year_loans = loans.filter(start_date__year=current_year).count()

    if current_year_loans == 0:
        return 80
    elif current_year_loans == 1:
        return 60  
    elif current_year_loans == 2:
        return 40  
    elif current_year_loans <= 4:
        return 20

def calculate_loan_approved_volume(customer,loans):
    if not loans.exists():
        return 50 
    total_loan_amount = loans.aggregate(total=Sum('loan_amount'))['total']  or 0

    annual_income = customer.monthly_salary*12

    if annual_income == 0:
        return 0
    
    loan_to_income_ratio = total_loan_amount / annual_income
        
    if loan_to_income_ratio <= 2:
        return 90  
    elif loan_to_income_ratio <= 4:
        return 70  
    elif loan_to_income_ratio <= 6:
        return 50  
    elif loan_to_income_ratio <= 8:
        return 30  
    else:
        return 10  
    
def calculate_loans_paid_on_time(loans):

    on_time_ratio =[]
    for loan in loans:
        if loan.tenure >0 :
            ratio = loan.emis_paid_on_time/loan.tenure
            on_time_ratio.append(ratio)
    payment_ratio = sum(on_time_ratio)/len(on_time_ratio)

    if payment_ratio >= 0.95:
        return 100
    elif payment_ratio >= 0.85:
        return 80
    elif payment_ratio >= 0.70:
        return 60
    elif payment_ratio >= 0.50:
        return 40
    else:
        return 20