import json
from decimal import Decimal
from .dates import parse_date
from .constants import BANK_REG_NUM

def validate_init_bank(request, ipbr_data):
    reg_num = ipbr_data['reg_num']
    target_hostname = ipbr_data['target_hostname']
    init_transfer_path = ipbr_data['init_transfer_path']
    pre_confirm_path = ipbr_data['pre_confirm_path']
    confirm_path = ipbr_data['confirm_path']
    cancel_path = ipbr_data['cancel_path']

    init_reg = request['init_reg']
    target_reg = request['target_reg']
    init_account = request['init_account']
    target_account = request['target_account']
    init_transaction_id = request['init_transaction_id']
    amount = request['amount']
    expires = request['expires']

    # if reg_num != init_reg or init_reg == BANK_REG_NUM:
    #     raise ValueError('Invalid init_reg')

    return {
        'init_reg': init_reg,
        'target_reg': target_reg,
        'init_account': init_account,
        'target_account': target_account,
        'init_transaction_id': init_transaction_id,
        'amount': amount,
        'expires': expires,
        'target_hostname': target_hostname,
        'init_transfer_path': init_transfer_path,
        'pre_confirm_path': pre_confirm_path,
        'confirm_path': confirm_path,
        'cancel_path': cancel_path
    }

def validate_init_transfer(request):
    # unpack json data
    data = json.loads(request.body)
    data = data['data']
    
    init_reg = data['init_reg']
    target_reg = data['target_reg']
    init_account = data['init_account']
    target_account = data['target_account']
    init_transaction_id = data['init_transaction_id']
    expires = data['expires']
    amount = data['amount']

    try:
        expires = parse_date(expires)
        amount = Decimal(amount)
    except:
        raise ValueError('Invalid input')
    
    # if init_reg == BANK_REG_NUM:
    #     raise ValueError('Invalid init_reg')

    # if target_reg != BANK_REG_NUM:
    #     raise ValueError('Invalid target_reg')

    if len(init_reg) != 4:
        raise ValueError('Invalid init_reg')
    
    if len(target_reg) != 4:
        raise ValueError('Invalid target_reg')
    
    if not init_transaction_id:
        raise ValueError('Invalid init_transaction_id')
    
    if not expires:
        raise ValueError('Invalid expires')
    
    if amount <= 0:
        raise ValueError('Invalid amount')

    
    return {
        'init_reg': init_reg,
        'target_reg': target_reg,
        'init_account': init_account,
        'target_account': target_account,
        'init_transaction_id': init_transaction_id,
        'amount': amount,
        'expires': expires
    }

def validate_pre_confirm_transfer(request):
    data = json.loads(request.body)
    data = data['data']

    init_reg = data['init_reg']
    target_reg = data['target_reg']
    init_account = data['init_account']
    target_account = data['target_account']
    init_transaction_id = data['init_transaction_id']
    target_transaction_id = data['target_transaction_id']
    expires = data['expires']
    amount = data['amount']

    try:
        expires = parse_date(expires)
        amount = Decimal(amount)
    except:
        raise ValueError('Invalid input')
    
    # if init_reg != BANK_REG_NUM:
    #     raise ValueError('Invalid init_reg')

    # if target_reg == BANK_REG_NUM:
    #     raise ValueError('Invalid target_reg')

    if len(init_reg) != 4:
        raise ValueError('Invalid init_reg')
    
    if len(target_reg) != 4:
        raise ValueError('Invalid target_reg')
    
    if not init_transaction_id:
        raise ValueError('Invalid init_transaction_id')
    
    if not target_transaction_id:
        raise ValueError('Invalid target_transaction_id')
    
    if not expires:
        raise ValueError('Invalid expires')
    
    if amount <= 0:
        raise ValueError('Invalid amount')

    
    return {
        'init_reg': init_reg,
        'target_reg': target_reg,
        'init_account': init_account,
        'target_account': target_account,
        'init_transaction_id': init_transaction_id,
        'target_transaction_id': target_transaction_id,
        'amount': amount,
        'expires_externally': expires
    }