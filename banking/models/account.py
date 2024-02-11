import random
from django.db import models
from banking.models.customer import Customer
from banking.utils.constants import BANK_REG_NUM
from banking.models.account_type import Account_type

def generate_account_number():
    return random.randint(1000000000, 9999999999)

class Account(models.Model):
    account_num = models.CharField(max_length=10, unique=True, default=generate_account_number) 
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    account_type = models.ForeignKey(Account_type, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def account_reg_num(self):
        return BANK_REG_NUM + ' ' + self.account_num


    def __str__(self):
        return self.name
    