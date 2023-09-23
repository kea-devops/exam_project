from django.db import models
from banking.models.customer import Customer
from banking.models.account_type import Account_type

class Account(models.Model):
    customerid = models.ForeignKey(Customer, on_delete=models.PROTECT)
    account_typeid = models.ForeignKey(Account_type, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)