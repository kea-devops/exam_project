from time import sleep
from .init_transfer import init_transfer
from .pre_confirm_transfer import pre_confirm_transfer
from .confirm_transfer import confirm_transfer

def rq_worker(params):
    job = params['job']
    print('Worker:', job)

    if job == 'init_transfer':
        sleep(1)
        init_transfer(params['data'])
    elif job == 'pre_confirm_transfer':
        sleep(1)
        pre_confirm_transfer(params['data'])
    elif job == 'confirm_transfer':
        sleep(1)
        confirm_transfer(params['data'])