from django.db import models
from django.contrib.auth.models import User
from banking.models.account import Account

class LoanApplication(models.Model):
      user = models.ForeignKey(User, on_delete=models.PROTECT)
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      account = models.ForeignKey(Account, on_delete=models.PROTECT)
