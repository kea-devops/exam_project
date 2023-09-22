from django.db import account 
from django.db import models
from models.customer import Customer
from models.account_type import Account_type

class Account(models.Model):
    customerid = models.ForeignKey(Customer)
    account_typeid = models.ForeignKey(Account_type)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)