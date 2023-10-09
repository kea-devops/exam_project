from django import forms
from banking.models.account import LoanApplication, Account


class LoanApplicationForm(forms.ModelForm):
      account = forms.ModelChoiceField(
           queryset=Account.objects.all(),
           empty_label=None,
           label='Select an account',
           widget=forms.Select(attrs={'class': 'form-control'}),
           to_field_name='name'
      )      


      class Meta:
           model = LoanApplication
           fields = ['amount', 'account']
