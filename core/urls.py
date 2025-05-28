from django.urls import path
from .views import CustomerRegisterView,CheckEligibilityView,CreateLoanView,LoanDetailsView
urlpatterns = [
     path('register/', CustomerRegisterView.as_view(), name='register-customer'),
     path('check-eligibility/', CheckEligibilityView.as_view(), name='check-eligibility'),
     path('create-loan/',CreateLoanView.as_view(),name='create-loan'),
     path('view-loan/<int:loan_id>/',LoanDetailsView.as_view(),name='view-loan')
]