from django.db import models
from banking.models.customer import Customer
from banking.models.account import Account

class LoanApplication(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='loan_applications')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('pre_approved', 'Pre-approved'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
