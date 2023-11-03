from django.db import models
from banking.models.customer import Customer
from banking.models.account import Account
from django.db import models, transaction


class Ledger(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    account_id = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def transfer(cls, amount, debit_account, debit_text, credit_account, credit_text, is_loan=False):
        if amount < 0:
            raise ValueError('The amout most be positive')

        with transaction.atomic():
            if debit_account.balance >= amount or is_loan:
                transaction = cls.objects.create(amount=amount, account=debit_account, text=debit_text)
                transaction.save()

                cls.objects.create(amount=-amount, transaction=transaction, account=credit_account, text=credit_text)
            else:
                raise ValueError('not enough funds available')

    def __str__(self):
        return f'{self.amount} :: {self.transaction} :: {self.timestamp} :: {self.account} :: {self.text}'