from django.db import models
from banking.models.customer import Customer
from banking.models.account_type import Account_type

class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    account_type = models.ForeignKey(Account_type, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    
    
class LoanApplication(models.Model):
      customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='loan_applications')
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      account = models.ForeignKey(Account, on_delete=models.PROTECT)
      STATUS_CHOICES = (
          ('pending', 'Pending Loan'),
          ('approved', 'Approved Loan'),
          ('approved_employee', 'Approved by Employee'),
          ('denied', 'Denied Loan'),
      )

      status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
      supervisor_approved = models.BooleanField(default=False)
