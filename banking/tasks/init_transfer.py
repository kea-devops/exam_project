import requests
from django.db import transaction
from banking.models.ipbt import IPBT
from banking.models.account import Account
from banking.models.customer import Customer
from banking.utils.constants import IPBR_URL
from banking.utils.dates import time_from_now
from banking.utils.errors import TransactionError
from banking.models.transaction import Transaction
from banking.models.account_type import Account_type
from banking.utils.ipbt_validation import validate_init_bank
from banking.utils.choices import IPBT_TYPE_CHOICES, IPBT_STATUS_CHOICES

def init_transfer(params):
    init_reg = params['init_reg']

    # Lookup init bank at IPBR
    try:
        response = requests.get(IPBR_URL + '/lookup/' + init_reg)
    except requests.exceptions.RequestException as e:
        print(e)
        return # Halt execution
    
    if response.status_code != 200:
        print('Invalid response from IPBR')
        return # Halt execution
    
    try:
        ipbr_data = response.json()['data']
        data = validate_init_bank(params, ipbr_data)
    except Exception as e:
        print(e)
        return # Halt execution
    
    # Perform PRE_CONFIRM request to init bank
    try:
        tnx = Transaction()
        expires = time_from_now(600)
        body = {
            'data': {
                'init_reg': data['init_reg'],
                'target_reg': data['target_reg'],
                'init_account': data['init_account'],
                'target_account': data['target_account'],
                'init_transaction_id': data['init_transaction_id'],
                'target_transaction_id': str(tnx.pk),
                'expires': expires,
                'amount': str(data['amount']),
            }
        }
        url = data['target_hostname'] + data['pre_confirm_path']
        response = requests.put(url, json=body)
    except requests.exceptions.RequestException as e:
        print(e)
        return
    
    if response.status_code != 200:
        print('Invalid response from init bank')
        return
    
    # Unwrap response from PRE_CONFIRM request
    try:
        response_data = response.json()
        authorized = response_data['authorized']
        init_reg = response_data['data']['init_reg']
        init_account = response_data['data']['init_account']
        target_account = response_data['data']['target_account']
        init_transaction_id = response_data['data']['init_transaction_id']
        expires_externally = response_data['data']['expires']
        amount = response_data['data']['amount']
    except Exception as e:
        print(e)
        return
    
    if not authorized:
        return
    
    # Lookup target account
    try:
        target_account = Account.objects.get(account_num=target_account)
    except Account.DoesNotExist as e:
        return # Halt execution


    # Create interbank account for target bank if not exists
    try:
        internal_customer = Customer.objects.get(email='internal_accounts')
    except Customer.DoesNotExist as e:
        return
    
    try:
        internal_accounts = Account.objects.get(customer=internal_customer, name=init_reg)
    except Account.DoesNotExist as e:
        try:
            account_type = Account_type.objects.get(name='Interbanking')
        except Account_type.DoesNotExist as e:
            raise TransactionError('Internal Server Error', status_code=500)
        internal_accounts = Account(
            customer=internal_customer,
            account_type=account_type,
            name=init_reg,
        )

    # Create pending IPB Transaction
    try:
        with transaction.atomic():
            expires_internally = time_from_now(600)
            ipbt = IPBT(
                transaction=tnx,
                transaction_target=init_transaction_id,
                internal_account=target_account,
                external_account=init_account,
                external_bank_reg=init_reg,
                amount=amount,
                type=IPBT_TYPE_CHOICES[1][0],
                status=IPBT_STATUS_CHOICES[3][0],
                target_hostname=data['target_hostname'],
                init_transfer_path=data['init_transfer_path'],
                pre_confirm_path=data['pre_confirm_path'],
                confirm_path=data['confirm_path'],
                cancel_path=data['cancel_path'],
                expires_internally_at=expires_internally,
                expires_externally_at=expires_externally,
            )
            internal_accounts.save()
            tnx.save()
            ipbt.save()
    except Exception as e:
        print('Create pending IPBT Error: ', e)

