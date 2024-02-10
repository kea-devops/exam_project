from django.db import models
from django.conf import settings
from banking.models.customer import Customer
from banking.models.account_type import Account_type

class Account(models.Model):
    account_num = models.CharField(max_length=10, unique=True) 
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    account_type = models.ForeignKey(Account_type, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def account_reg_num(self):
        return getattr(settings, 'BANK_REG_NUM', None) + ' ' + self.account_num


    def __str__(self):
        return self.name
    