from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Customer(models.Model):
    class CustomerRank(models.TextChoices):
        BLUE = 'BLUE', _('Blue')
        SILVER = 'SILVER', _('Silver')
        GOLD = 'GOLD', _('Gold')
    user_id = models.ForeignKey(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)