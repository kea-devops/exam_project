import django_rq

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from banking.models.ipbt import IPBT
from banking.models.ledger import Ledger
from banking.models.account import Account
from banking.models.customer import Customer
from banking.tasks.worker import rq_worker
from banking.utils.dates import time_from_now
from banking.utils.choices import IPBT_STATUS_CHOICES, TRANSACTION_TYPE_CHOICES
from banking.utils.ipbt_validation import validate_init_transfer, validate_pre_confirm_transfer

@csrf_exempt
def init_transfer(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)
    if not request.headers.get('Content-Type') == 'application/json':
        return HttpResponse('Unsupported Media Type', status=415)
    
    try:
        data = validate_init_transfer(request)
    except ValueError as e:
        return HttpResponse(str(e), status=400)
    
    account = get_object_or_404(Account, account_num=data['target_account'])

    params = { 'job': 'init_transfer', 'data': data}
    django_rq.enqueue(rq_worker, params)

    return JsonResponse({
        'data': {
            'init_transaction_id': data['init_transaction_id'],
            'init_reg': data['init_reg'],
            'target_reg': data['target_reg'],
            'init_account': data['init_account'],
            'target_account': account.account_num,
            'amount': data['amount'],
            'expires': data['expires']
        },
        'authorized': True,
    }, status=200)


@csrf_exempt
def pre_confirm_transfer(request):
    if request.method != 'PUT':
        return HttpResponse('Method not allowed', status=405)
    if not request.headers.get('Content-Type') == 'application/json':
        return HttpResponse('Unsupported Media Type', status=415)
    
    try:
        data = validate_pre_confirm_transfer(request)
    except ValueError as e:
        return HttpResponse(str(e), status=400)
    
    ipbt = get_object_or_404(IPBT, transaction=data['init_transaction_id'])
    try:
        account = Account.objects.get(account_num=data['target_account'])
    except:
        ipbt.status = IPBT_STATUS_CHOICES[4][0]
        ipbt.expires_internally_at = None
        ipbt.expires_externally_at = None
        ipbt.save()
        

    expires_at = time_from_now(10)
    data['expires_internally'] = expires_at
    
    params = { 'job': 'pre_confirm_transfer', 'data': data}
    django_rq.enqueue(rq_worker, params)

    return JsonResponse({
        'data': {
            'init_transaction_id': str(ipbt.pk),
            'init_reg': data['init_reg'],
            'target_reg': data['target_reg'],
            'init_account': data['init_account'],
            'target_account': account.account_num,
            'amount': data['amount'],
            'expires': str(expires_at)
        },
        'authorized': True,
    }, status=200)


@csrf_exempt
def confirm_transfer(request):
    if request.method != 'PUT':
        return HttpResponse('Method not allowed', status=405)
    if not request.headers.get('Content-Type') == 'application/json':
        return HttpResponse('Unsupported Media Type', status=415)
    
    try:
        data = validate_pre_confirm_transfer(request)
    except ValueError as e:
        print('Confirm Transfer Data Error:', e)
        return HttpResponse(str(e), status=400)

    # Create ledger entries and update IPBT status
    try:
        ipbt = IPBT.objects.get(transaction_id=data['target_transaction_id'])
        target_account = ipbt.internal_account
        internal_customer = Customer.objects.get(email='internal_accounts')
        internal_account = Account.objects.get(customer=internal_customer, name=ipbt.external_bank_reg)
        transfer_type = TRANSACTION_TYPE_CHOICES[2][0]

        counterparty = ipbt.external_bank_reg + ' ' + ipbt.external_account
        ledger_entry_debit = Ledger(
            transaction=ipbt.transaction,
            account=target_account,
            amount=ipbt.amount,
            counterparty=counterparty,
            type=transfer_type
        )
        ledger_entry_credit = Ledger(
            transaction=ipbt.transaction,
            account=internal_account,
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
    except:
        # TODO: Send a CANCEL request to the init bank
        return HttpResponse('Invalid target_transaction_id', status=400)
    
    return JsonResponse({
        'data': {
            'init_transaction_id': str(ipbt.pk),
            'init_reg': data['init_reg'],
            'target_reg': data['target_reg'],
            'init_account': data['init_account'],
            'target_account': target_account.account_num,
            'amount': data['amount'],
            'expires': None
        },
        'authorized': True,
    }, status=200)


@csrf_exempt
def cancel_transfer(request):
    # TODO: Implement this view
    pass
