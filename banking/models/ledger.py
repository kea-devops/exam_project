from uuid import uuid4
from django.db import models
from banking.models.customer import Customer
from banking.models.account import Account
from django.db.models import Sum, Q

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

class Ledger(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

def generate_balance(accounts):
    for account in accounts:
        balance = Ledger.objects.filter(account=account).aggregate(Sum('amount'))['amount__sum']
        if balance is None:
            account.balance = 0
        else:
            account.balance = balance
        account.balance = '{0:.2f}'.format(account.balance)
    return accounts

def append_counterpart(movements):
    for movement in movements:
        counterpart = Ledger.objects.filter(~Q(account=movement.account), transaction=movement.transaction).select_related('account').first()
        movement.counterpart = counterpart.account
    return movements