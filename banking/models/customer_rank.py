from django.db import models

class Customer_rank(models.Model):
    name = models.CharField(max_length=50, unique=True)
    score = models.IntegerField()