from django.db import models

STATUS_CHOICES = (
    ('pending_out', 'Pending (Outgoing)'),
    ('pending_in', 'Pending (Incoming)'),
    ('confirmed_out', 'Confirmed (Outgoing)'),
    ('confirmed_in', 'Confirmed (Incoming)'),
    ('failed_out', 'Failed (Outgoing)'),
    ('failed_in', 'Failed (Incoming)'),
    ('cancelled_out', 'Cancelled (Outgoing)'),
    ('cancelled_in', 'Cancelled (Incoming)'),
    ('completed_out', 'Completed (Outgoing)'),
    ('completed_in', 'Completed (Incoming)'),
)

TYPE_CHOICES = (
    ('transfer_out', 'Transfer (Outgoing)'),
    ('transfer_in', 'Transfer (Incoming)'),
)

# Interplanetary Banking Transactions
class IPBT(models.Model):
    account = models.ForeignKey('Account', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    