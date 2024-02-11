from django.db import models
from banking.utils.choices import IPBT_STATUS_CHOICES, IPBT_TYPE_CHOICES

# Interplanetary Banking Transactions
class IPBT(models.Model):
    transaction = models.ForeignKey('Transaction', null=True, on_delete=models.PROTECT)
    transaction_target = models.CharField(max_length=255, null=True)
    internal_account = models.ForeignKey('Account', on_delete=models.PROTECT)
    external_account = models.CharField(max_length=10, null=False)
    external_bank_reg = models.CharField(max_length=4, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=IPBT_TYPE_CHOICES, null=False)
    status = models.CharField(max_length=20, choices=IPBT_STATUS_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_internally_at = models.DateTimeField(null=True)
    expires_externally_at = models.DateTimeField(null=True)

    # The HTTP hostname url of the target bank
    target_hostname = models.CharField(max_length=255, null=False)
    # The path of the target bank's API to initialize the transaction
    init_transfer_path = models.CharField(max_length=255, null=False)
    # The path of the target bank's API to confirm the transaction
    pre_confirm_path = models.CharField(max_length=255, null=False)
    # The path of the target bank's API to confirm the transaction
    confirm_path = models.CharField(max_length=255, null=False)
    # The path of the target bank's API to cancel the transaction
    cancel_path = models.CharField(max_length=255, null=False)

    def init_url(self):
        return self.target_hostname + self.init_transfer_path
    
    def pre_confirm_url(self):
        return self.target_hostname + self.pre_confirm_path
    
    def confirm_url(self):
        return self.target_hostname + self.confirm_path
    
    def cancel_url(self):
        return self.target_hostname + self.cancel_path
    