TRANSACTION_TYPE_CHOICES = (
    ('loan_deposit', 'Loan Deposit'),           # [0]
    ('internal_transfer', 'Internal Transfer'), # [1]
    ('external_transfer', 'External Transfer'), # [2]
    ('deposit', 'Deposit'),                     # [3]
    ('withdrawal', 'Withdrawal'),               # [4]
    ('payment', 'Payment'),                     # [5]
    ('fee', 'Fee'),                             # [6]
    ('interest', 'Interest'),                   # [7]
)

LOAN_APPLICATION_STATUS_CHOICES = (
    ('pending', 'Pending Approval'),
    ('pre_approved', 'Pre-approved'),
    ('approved', 'Approved'),
    ('denied', 'Denied'),
)

IPBT_STATUS_CHOICES = (
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

IPBT_TYPE_CHOICES = (
    ('transfer_out', 'Transfer (Outgoing)'),
    ('transfer_in', 'Transfer (Incoming)'),
)

def choices_to_list(choices):
    return [choice[0] for choice in choices]