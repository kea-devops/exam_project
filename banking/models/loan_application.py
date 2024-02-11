from django.db import models
from banking.models.customer import Customer
from banking.models.account import Account
from banking.utils.choices import LOAN_APPLICATION_STATUS_CHOICES

class LoanApplication(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='loan_applications')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=LOAN_APPLICATION_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
