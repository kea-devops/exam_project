import random
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password        
from django.contrib.auth.models import User
from django.db.models import DateTimeField
from django.conf import settings
from banking.models.ledger import Ledger
from banking.models.account import Account
from banking.models.customer import Customer
from banking.models.transaction import Transaction
from banking.models.account_type import Account_type
from banking.models.customer_rank import Customer_rank

def account_number():
    return random.randint(1000000000, 9999999999)

def counterparty(account):
    return getattr(settings, 'BANK_REG_NUM', None) + ' ' + str(account.account_num)

# Demo Customers
user1 = User(username="bob@johnson.com", email="bob@johnson.com", first_name="Bob", last_name="Johnson", password=make_password("123456"))
customer1 = Customer(user = user1, rank = Customer_rank.objects.get(name="Blue"), first_name = user1.first_name, last_name = user1.last_name, email = user1.email, phone = "12345678", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True),)
account11 = Account(customer = customer1, account_num = account_number(), account_type = Account_type.objects.get(name="Regular"), name = "Nemkonto", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True),)
account12 = Account(customer = customer1, account_num = account_number(), account_type = Account_type.objects.get(name="Savings"),name = "Opsparingskonto",created_at = DateTimeField(auto_now_add=True),updated_at = DateTimeField(auto_now=True),)
account13 = Account(customer = customer1, account_num = account_number(), account_type = Account_type.objects.get(name="Loan"),name = "Billån", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True),)

user2 = User(username="john@bobson.com", email="john@bobson.com", first_name="John", last_name="Bobson", password=make_password("123456"))
customer2 = Customer(user = user2, rank = Customer_rank.objects.get(name="Silver"), first_name = user2.first_name, last_name = user2.last_name, email = user2.email, phone = "87654321", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True))
account21 = Account(customer = customer2, account_num = account_number(), account_type = Account_type.objects.get(name="Regular"), name = "Nemkonto", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True))
account22 = Account(customer = customer2, account_num = account_number(), account_type = Account_type.objects.get(name="Savings"), name = "Opsparingskonto", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True))
account23 = Account(customer = customer2, account_num = account_number(), account_type = Account_type.objects.get(name="Loan"), name = "Billån", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True))

user3 = User(username="jane@johnson.com", email="jane@johnson.com", first_name="Jane", last_name="Johnson", password=make_password("123456"))
customer3 = Customer(user = user3, rank = Customer_rank.objects.get(name="Gold"),first_name = user3.first_name, last_name = user3.last_name,email = user3.email, phone = "12348765", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True),)
account31 = Account(customer = customer3, account_num = account_number(), account_type = Account_type.objects.get(name="Regular"), name = "Nemkonto", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True))
account32 = Account(customer = customer3, account_num = account_number(), account_type = Account_type.objects.get(name="Savings"), name = "Opsparingskonto", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True))
account33 = Account(customer = customer3, account_num = account_number(), account_type = Account_type.objects.get(name="Loan"), name = "Billån", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True))

# Demo User 1 Loan
transaction1 = Transaction()
ledger11 = Ledger(transaction = transaction1, type = 'loan_deposit', account = account11, amount = 1000, created_at = DateTimeField(auto_now_add=True))
ledger12 = Ledger(transaction = transaction1, type = 'loan_deposit', account = account13, amount = -1000, created_at = DateTimeField(auto_now_add=True))

# Demo User 2 Loan
transaction2 = Transaction()
ledger21 = Ledger(transaction = transaction2, type = 'loan_deposit', account = account21, amount = 1000, created_at = DateTimeField(auto_now_add=True))
ledger22 = Ledger(transaction = transaction2, type = 'loan_deposit', account = account23, amount = -1000, created_at = DateTimeField(auto_now_add=True))

# Demo User 3 Loan
transaction3 = Transaction()
ledger31 = Ledger(transaction = transaction3, type = 'loan_deposit', account = account31, amount = 1000, created_at = DateTimeField(auto_now_add=True))
ledger32 = Ledger(transaction = transaction3, type = 'loan_deposit', account = account33, amount = -1000, created_at = DateTimeField(auto_now_add=True))

# Demo User 1 to User 2
transaction4 = Transaction()
ledger11_21 = Ledger(transaction = transaction4, type = 'internal_transfer', account = account11, counterparty = counterparty(account21), amount = -500, created_at = DateTimeField(auto_now_add=True))
ledger21_11 = Ledger(transaction = transaction4, type = 'internal_transfer', account = account21, counterparty = counterparty(account11), amount = 500, created_at = DateTimeField(auto_now_add=True))

# Demo User 2 to User 3
transaction5 = Transaction()
ledger21_31 = Ledger(transaction = transaction5, type = 'internal_transfer', account = account21, counterparty = counterparty(account31), amount = -250, created_at = DateTimeField(auto_now_add=True))
ledger31_21 = Ledger(transaction = transaction5, type = 'internal_transfer', account = account31, counterparty = counterparty(account21), amount = 250, created_at = DateTimeField(auto_now_add=True))

# Demo User 3 to User 1
transaction6 = Transaction()
ledger31_11 = Ledger(transaction = transaction6, type = 'internal_transfer', account = account31, counterparty = counterparty(account11), amount = -100, created_at = DateTimeField(auto_now_add=True))
ledger11_31 = Ledger(transaction = transaction6, type = 'internal_transfer', account = account11, counterparty = counterparty(account31), amount = 100, created_at = DateTimeField(auto_now_add=True))

class Command(BaseCommand):
    def handle(self, **options):
        from django.db import transaction
        with transaction.atomic():
            self.create_demo_data()

    def create_demo_data(self):
        # Demo User 1
        user1.save()
        customer1.save()
        account11.save()
        account12.save()
        account13.save()
        
        # Demo User 2
        user2.save()
        customer2.save()
        account21.save()
        account22.save()
        account23.save()
        
        # Demo User 3
        user3.save()
        customer3.save()
        account31.save()
        account32.save()
        account33.save()

        # Demo User 1 Loan
        transaction1.save()
        ledger11.save()
        ledger12.save()

        # Demo User 2 Loan
        transaction2.save()
        ledger21.save()
        ledger22.save()

        # Demo User 3 Loan
        transaction3.save()
        ledger31.save()
        ledger32.save()

        # Demo User 1 to User 2
        transaction4.save()
        ledger11_21.save()
        ledger21_11.save()

        # Demo User 2 to User 3
        transaction5.save()
        ledger21_31.save()
        ledger31_21.save()

        # Demo User 3 to User 1
        transaction6.save()
        ledger31_11.save()
        ledger11_31.save()

        print("Demo data created successfully")
        
