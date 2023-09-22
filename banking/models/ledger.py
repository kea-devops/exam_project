from django.db import models
from models.customer import Customer
from models.account import Account


class Ledger(models.Model):
    costumer_id = models.ForeignKey(Customer)
    account_id = models.ForeignKey(Account)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)