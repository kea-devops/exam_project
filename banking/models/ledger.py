from django.db import models
from django.conf import settings
from django.db.models import Sum, Q
from banking.models.account import Account
from banking.models.transaction import Transaction

TRANSACTION_TYPES = (
    ('loan_deposit', 'Loan Deposit'),           # [0]
    ('internal_transfer', 'Internal Transfer'), # [1]
    ('external_transfer', 'External Transfer'), # [2]
    ('deposit', 'Deposit'),                     # [3]
    ('withdrawal', 'Withdrawal'),               # [4]
    ('payment', 'Payment'),                     # [5]
    ('fee', 'Fee'),                             # [6]
    ('interest', 'Interest'),                   # [7]
)

class Ledger(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    counterparty = models.CharField(max_length=15)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, blank=False, null=False)
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
