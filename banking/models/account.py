from django.db import account 
from django.db import models
from models.customer import Customer

class Account(models.Model):
    customerid = models.ForeignKey(Customer)
    account_typeid = models.ForeignKey(account_type)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)