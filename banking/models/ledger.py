from django.db import models
from banking.models.customer import Customer
from banking.models.account import Account
from django.db.models import Sum

class Ledger(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    account_id = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

def generate_balance(accounts):
    for account in accounts:
        balance = Ledger.objects.filter(account_id=account).aggregate(Sum('amount'))['amount__sum']
        if balance is None:
            account.balance = 0
        else:
            account.balance = balance
        account.balance = '{0:.2f}'.format(account.balance)
    return accounts