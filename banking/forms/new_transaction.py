from django import forms
from django.conf import settings
from banking.models.account import Account
from banking.models.ledger import Ledger, get_balance, TRANSACTION_TYPES
from banking.models.transaction import Transaction
from django.db import transaction

class TransactionError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = 500
    pass

class TransactionForm(forms.ModelForm):
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        empty_label=None,
        label='From account',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    recipient_reg_num = forms.CharField(
        label='Registration number',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=4,
    )
    recipient_account = forms.CharField(
        label='Account number',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=10,
    )
    amount = forms.DecimalField(
        label='Amount',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_digits=10,
        decimal_places=2,
    )

    def process(self, user):
        bank_reg = getattr(settings, 'BANK_REG_NUM', None)

        data = self.cleaned_data
        credit_account = data['account']
        amount = data['amount']

        # Check if the amount is positive
        if amount < 0:
            raise TransactionError('Amount must be positive', status_code=400)
        
        # Check if the customer is the owner of the account
        if credit_account.customer.user.pk != user.pk:
            raise TransactionError('You are not the owner of this account', status_code=403)
        
        # Check if the customer has enough funds in the relevant account
        balance = get_balance(credit_account)
        if balance < data['amount']:
            raise TransactionError('Insufficient funds', status_code=400)
        
        # Check if the recipient account exists
        
        debit_reg = data['recipient_reg_num']

        # Internal transfer
        if debit_reg == bank_reg:
            transfer_type = TRANSACTION_TYPES[1][0]
            try:
                debit_account = Account.objects.get(
                    account_num=data['recipient_account'],
                )
            except Account.DoesNotExist:
                raise TransactionError('Recipient account does not exist', status_code=400)
            debit_counterparty = debit_account.account_reg_num()

        # External transfer
        else:
            # TODO: Handle external transfers
            transfer_type = TRANSACTION_TYPES[2][0]
            raise TransactionError('External transfers are not supported', status_code=501)
        
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
                print('Transaction started')
                tnx.save()
                ledger_entry_debit.save()
                ledger_entry_credit.save()
        except Exception as e:
            print(e)    
            raise TransactionError('Transaction failed, please try again later', status_code=500)

        return credit_account.pk

    def __init__(self, customer, *args, **kwargs):
          super(TransactionForm, self).__init__(*args, **kwargs)
          self.fields['account'].queryset = Account.objects.filter(customer=customer).exclude(account_type__name='Loan')

    class Meta:
        model = Transaction
        fields = ('account', 'recipient_reg_num', 'recipient_account', 'amount')