from django import forms
from banking.models.account import Account
from banking.models.ledger import get_balance
from banking.utils.constants import BANK_REG_NUM
from banking.utils.errors import TransactionError
from banking.models.transaction import Transaction
import banking.utils.handle_transactions as transactions

class TransactionForm(forms.ModelForm):
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        empty_label=None,
        label='From account',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    target_reg_num = forms.CharField(
        label='Registration number',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=4,
    )
    target_account = forms.CharField(
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
        
        target_reg = data['target_reg_num']
        if target_reg == BANK_REG_NUM:
            return transactions.internal(data)
        else:
            return transactions.external(data)
        

    def __init__(self, customer, *args, **kwargs):
          super(TransactionForm, self).__init__(*args, **kwargs)
          self.fields['account'].queryset = Account.objects.filter(customer=customer).exclude(account_type__name='Loan')

    class Meta:
        model = Transaction
        fields = ('account', 'target_reg_num', 'target_account', 'amount')