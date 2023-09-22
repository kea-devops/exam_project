from django.db import models

class Account_type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    interest_rate = models.DecimalField(max_digits=2, decimal_places=2)