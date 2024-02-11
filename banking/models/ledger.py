from django.db import models
from django.db.models import Sum, Q
from banking.models.account import Account
from banking.models.transaction import Transaction
from banking.utils.choices import TRANSACTION_TYPE_CHOICES

class Ledger(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    counterparty = models.CharField(max_length=15)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

def get_balance(account):
    balance = Ledger.objects.filter(account=account).aggregate(Sum('amount'))['amount__sum']
    if balance is None:
        balance = 0
    return balance

def get_balances(accounts):
    for account in accounts:
        balance = get_balance(account)
        account.balance = '{0:.2f}'.format(balance)
    return accounts
