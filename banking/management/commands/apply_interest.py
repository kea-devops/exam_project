from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, **options):
        from banking.utils.choices import TRANSACTION_TYPE_CHOICES
        from banking.models.ledger import Ledger, get_balance
        from banking.models.account_type import Account_type
        from banking.models.transaction import Transaction
        from banking.models.customer import Customer
        from django.contrib.auth.models import User
        from banking.models.account import Account
        from django.db import transaction
        from decimal import Decimal
        
        interest_account, _ = Account.objects.get_or_create(
            account_type = Account_type.objects.get(name='Interest'),
            customer = Customer.objects.get(user=User.objects.get(username='internal_accounts')),
            name = 'Interest',
        )

        for account in Account.objects.all():
            interest_rate = account.account_type.interest_rate
            balance = get_balance(account)
            amount = balance * (interest_rate / Decimal(100))
            if interest_account == 0 or amount == 0:
                continue

            transfer_type = TRANSACTION_TYPE_CHOICES[7][0]
            tnx = Transaction()
            
            ledger_entry_debit = Ledger(
                transaction=tnx,
                account=account,
                amount=amount,
                counterparty='Interest',
                type=transfer_type
            )
            ledger_entry_credit = Ledger(
                transaction=tnx,
                account=interest_account,
                amount=-amount,
                counterparty='',
                type=transfer_type
            )
            with transaction.atomic():
                ledger_entry_debit.save()
                ledger_entry_credit.save()
                tnx.save()

    print('Interest applied successfully')
        