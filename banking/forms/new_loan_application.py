from django import forms
from banking.models.account import Account
from banking.models.loan_application import LoanApplication


class LoanApplicationForm(forms.ModelForm):
     account = forms.ModelChoiceField(
          queryset=Account.objects.all(),
          empty_label=None,
          label='Select an account',
          widget=forms.Select(attrs={'class': 'form-control'}),
     )

     def __init__(self, customer, *args, **kwargs):
          super(LoanApplicationForm, self).__init__(*args, **kwargs)
          self.fields['account'].queryset = Account.objects.filter(customer=customer).exclude(account_type__name='Loan')

     class Meta:
          model = LoanApplication
          fields = ['amount', 'account']
