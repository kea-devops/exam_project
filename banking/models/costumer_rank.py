from django.db import models

class Costumer_rank(models.Model):
    name = models.CharField(max_length=50, unique=True)