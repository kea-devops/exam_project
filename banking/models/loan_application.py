from django.db import models
from banking.models.customer import Customer
from banking.models.account import Account

class LoanApplication(models.Model):
      customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='loan_applications')
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      account = models.ForeignKey(Account, on_delete=models.PROTECT)
      STATUS_CHOICES = (
          ('pending', 'Pending Loan'),
          ('approved_employee', 'Pending Supervisor Approval'),
          ('approved', 'Approved Loan'),
          ('denied', 'Denied Loan'),
      )

      status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
      supervisor_approved = models.BooleanField(default=False)
