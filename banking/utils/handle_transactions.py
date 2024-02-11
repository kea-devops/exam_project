import requests
from django.db import transaction
from banking.models.ipbt import IPBT
from banking.models.ledger import Ledger
from banking.models.account import Account
from banking.models.customer import Customer
from banking.models.transaction import Transaction
from banking.models.account_type import Account_type
from banking.utils.choices import TRANSACTION_TYPE_CHOICES
from banking.utils.constants import IPBR_URL, BANK_REG_NUM
from banking.utils.errors import TransactionError
from banking.utils.dates import time_from_now
from banking.utils.choices import IPBT_TYPE_CHOICES, IPBT_STATUS_CHOICES

def internal(data):
    credit_account = data['account']
    amount = data['amount']
    transfer_type = TRANSACTION_TYPE_CHOICES[1][0]

    try:
        debit_account = Account.objects.get(account_num=data['recipient_account'])
    except Account.DoesNotExist:
        raise TransactionError('Recipient account does not exist', status_code=400)
    debit_counterparty = debit_account.account_reg_num()

    tnx = Transaction()
    ledger_entry_debit = Ledger(
        transaction=tnx,
        account=debit_account,
        amount=amount,
        counterparty=credit_account.account_reg_num(),
        type=transfer_type
    )
    ledger_entry_credit = Ledger(
        transaction=tnx,
        account=credit_account,
        amount=-amount,
        counterparty=debit_counterparty,
        type=transfer_type
    )

    try:
        with transaction.atomic():
            tnx.save()
            ledger_entry_debit.save()
            ledger_entry_credit.save()
    except Exception as e:
        print(e)
        raise TransactionError('Transaction failed, please try again later', status_code=500)

    return credit_account.pk

def external(transaction_data):
    # Unwrap transaction data
    try:
        account = transaction_data['account']
        amount = transaction_data['amount']
        target_account = transaction_data['target_account']
        target_reg = transaction_data['target_reg_num']
    except KeyError as e:
        print('KeyError:', e)
        raise TransactionError('Invalid transaction data', status_code=400)
    
    # Lookup target bank at IPBR
    try:
        response = requests.get(IPBR_URL + '/lookup/' + target_reg)
    except requests.exceptions.RequestException as e:
        print('Lookup Error:', e)
        raise TransactionError('Internal Server Error', status_code=500)
    
    if response.status_code != 200:
        raise TransactionError('Recipient bank not found', status_code=404)
    
    data = response.json()['data']
    
    # Prepare request to initiate transfer at target bank
    host = data['target_hostname']
    init_transfer_path = data['init_transfer_path']
    pre_confirm_path = data['pre_confirm_path']
    confirm_path = data['confirm_path']
    cancel_path = data['cancel_path']

    url = host + init_transfer_path
    tnx = Transaction()
    expires_at = time_from_now(600)
    body = {
        'data': {
			'init_reg': BANK_REG_NUM,
			'target_reg': target_reg,
			'init_account': account.account_num,
			'target_account': target_account,
			'init_transaction_id': str(tnx.pk),
			'expires': str(expires_at),
			'amount': str(amount),
		}
    }

    # Send INIT_TRANSFER request to target bank
    try:
        response = requests.post(url, json=body)
    except requests.exceptions.RequestException as e:
        print(e)
        raise TransactionError('Internal Server Error', status_code=500)
    
    if response.status_code != 200:
        raise TransactionError('Internal Server Error', status_code=500)
    
    # Validate response from target bank
    try:
        json = response.json()
        if not json['authorized']:
            raise TransactionError('Transaction not authorized', status_code=401)
        if not json['data']:
            raise TransactionError('Invalid response from target bank', status_code=500)
    
        # TODO: Ideally we would validate the response data here
    
    except ValueError as e:
        print(e)
        raise TransactionError('Invalid response from target bank', status_code=500)

    # Create interbank account for target bank if not exists
    try:
        internal_accounts = Customer.objects.get(email='internal_accounts')
    except Customer.DoesNotExist as e:
        raise TransactionError('Internal Server Error', status_code=500)
    
    try:
        Account.objects.get(customer=internal_accounts, name=target_reg)
    except Account.DoesNotExist as e:
        try:
            account_type = Account_type.objects.get(name='Interbanking')
        except Account_type.DoesNotExist as e:
            raise TransactionError('Internal Server Error', status_code=500)
        Account.objects.create(
            customer=internal_accounts,
            account_type=account_type,
            name=target_reg,
        )
        
    # Create pending IPB Transaction
    try:
        with transaction.atomic():
            ipbt = IPBT(
                transaction=tnx,
                transaction_target=None,
                internal_account=account,
                external_account=target_account,
                external_bank_reg=target_reg,
                amount=amount,
                type=IPBT_TYPE_CHOICES[0][0],
                status=IPBT_STATUS_CHOICES[0][0],
                expires_internally_at=expires_at,
                expires_externally_at=None,
                target_hostname=host,
                init_transfer_path=init_transfer_path,
                pre_confirm_path=pre_confirm_path,
                confirm_path=confirm_path,
                cancel_path=cancel_path,
            )
            tnx.save()
            ipbt.save()
    except Exception as e:
        print(e)
        raise TransactionError('Internal Server Error', status_code=500)

    # TODO: create cron job to check for expired transactions and fail them

    # Return
    return account.pk