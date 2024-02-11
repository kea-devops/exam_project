from django.core.management.base import BaseCommand
from banking.models.customer_rank import Customer_rank

class Command(BaseCommand):
    def handle(self, **options):
        from django.contrib.auth.models import User
        from django.contrib.auth.hashers import make_password
        from banking.models.account_type import Account_type
        from banking.models.customer import Customer
        from decimal import Decimal
        
        # Create admin if not exists and give staff and superuser permissions
        admin, admin_created = User.objects.get_or_create(username='admin')
        if admin_created:
            admin.is_staff = True
            admin.is_superuser = False
            admin.password = make_password('123456')
            admin.save()

        supervisor, supervisor_created = User.objects.get_or_create(username='supervisor')
        if supervisor_created:
            supervisor.is_staff = True
            supervisor.is_superuser = True
            supervisor.password = make_password('123456')
            supervisor.save()

        # Create customers ranks if table is empty
        if not Customer_rank.objects.all():
            Customer_rank.objects.create(name='Blue', score=1)
            Customer_rank.objects.create(name='Silver', score=25)
            Customer_rank.objects.create(name='Gold', score=75)

        # Create account types if table is empty
        if not Account_type.objects.all():
            Account_type.objects.create(name='Regular', internal_use=False, interest_rate=Decimal(2.10))
            Account_type.objects.create(name='Savings', internal_use=False, interest_rate=Decimal(5.75))
            Account_type.objects.create(name='Loan', internal_use=True, interest_rate=Decimal(12.32))
            Account_type.objects.create(name='Interbanking', internal_use=True, interest_rate=Decimal(0))

        internal_accounts, internal_accounts_created = User.objects.get_or_create(username='internal_accounts')
        if internal_accounts_created:
            internal_accounts.is_staff = True
            internal_accounts.is_superuser = True
            internal_accounts.password = make_password('123456')
            internal_accounts.save()

        try:
            Customer.objects.get(user=internal_accounts)
        except Customer.DoesNotExist:
            Customer.objects.create(
                    user = internal_accounts,
                    rank = Customer_rank.objects.get(name='Blue'),
                    first_name = 'Internal',
                    last_name = 'Accounts',
                    email = 'internal_accounts',
                    phone = '00000000'
                )

        print('Provisioning completed successfully')