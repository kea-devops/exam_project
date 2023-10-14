from django.db import models
from django.contrib.auth.models import User
from .costumer_rank import Customer_rank

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    customer_rank = models.ForeignKey(Customer_rank, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
