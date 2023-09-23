from django.db import models
from banking.models.customer import Customer
from banking.models.account import Account


class Ledger(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    account_id = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)