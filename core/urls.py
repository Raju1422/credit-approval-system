from django.urls import path
from .views import CustomerRegisterView,CheckEligibilityView,CreateLoanView
urlpatterns = [
     path('register/', CustomerRegisterView.as_view(), name='register-customer'),
     path('check-eligibility/', CheckEligibilityView.as_view(), name='check-eligibility'),
     path('create-loan/',CreateLoanView.as_view(),name='create-loan')
]