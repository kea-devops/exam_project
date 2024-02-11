import requests
from django.db import transaction
from banking.models.ipbt import IPBT
from banking.models.ledger import Ledger
from banking.models.account import Account
from banking.models.customer import Customer
from banking.utils.choices import IPBT_STATUS_CHOICES, TRANSACTION_TYPE_CHOICES


def pre_confirm_transfer(params):
    init_reg = params['init_reg']
    target_reg = params['target_reg']
    init_account = params['init_account']
    target_account = params['target_account']
    init_transaction_id = params['init_transaction_id']
    target_transaction_id = params['target_transaction_id']
    amount = params['amount']
    expires_internally = params['expires_internally']
    expires_externally = params['expires_externally']

    ipbt = IPBT.objects.get(transaction_id=params['init_transaction_id'])

    # Send CONFIRM request to the target bank
    try:
        body = {
            'data': {
                'init_reg': init_reg,
                'target_reg': target_reg,
                'init_account': init_account,
                'target_account': target_account,
                'init_transaction_id': init_transaction_id,
                'target_transaction_id': target_transaction_id,
                'expires': expires_internally,
                'amount': str(amount),
            }
        }
        url = ipbt.target_hostname + ipbt.confirm_path
        response = requests.put(url, json=body)
        response.raise_for_status()
        confirm_data = response.json()
        if not confirm_data['authorized']:
            raise ValueError('Unauthorized')
    except Exception as e:
        print('CONFIRM Request Error:', e)
        ipbt.status = IPBT_STATUS_CHOICES[4][0]
        ipbt.expires_internally_at = None
        ipbt.expires_externally_at = None
        ipbt.save()
        return # Halt execution

    # Create ledger entries and update IPBT status
    try:
        init_account = ipbt.internal_account
        internal_customer = Customer.objects.get(email='internal_accounts')
        internal_account = Account.objects.get(customer=internal_customer, name=ipbt.external_bank_reg)
        transfer_type = TRANSACTION_TYPE_CHOICES[2][0]

        counterparty = ipbt.external_bank_reg + ' ' + ipbt.external_account
        ledger_entry_debit = Ledger(
            transaction=ipbt.transaction,
            account=internal_account,
            amount=ipbt.amount,
            counterparty=counterparty,
            type=transfer_type
        )
        ledger_entry_credit = Ledger(
            transaction=ipbt.transaction,
            account=init_account,
            amount=-ipbt.amount,
            counterparty=counterparty,
            type=transfer_type
        )

        ipbt.status = IPBT_STATUS_CHOICES[9][0]
        ipbt.expires_internally_at = None
        ipbt.expires_externally_at = None

        with transaction.atomic():
            ledger_entry_debit.save()
            ledger_entry_credit.save()
            ipbt.save()
        
    except Exception as e:
        print('Create Ledger Error:', e)
        ipbt.status = IPBT_STATUS_CHOICES[4][0]
        ipbt.expires_internally_at = None
        ipbt.expires_externally_at = None
        ipbt.save()
        return
    
    # ipbt.save()