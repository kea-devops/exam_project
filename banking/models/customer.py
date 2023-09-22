from django.db import models
from django.contrib.auth.models import User
from models.costumer_rank import Costumer_rank

class Customer(models.Model):
    user_id = models.ForeignKey(User)
    costumer_rank_id = models.ForeignKey(Costumer_rank)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
