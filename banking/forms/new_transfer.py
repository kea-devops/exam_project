from django.forms import ModelForm, CharField, EmailField, ChoiceField, PasswordInput, DecimalField, IntegerField
from django.contrib.auth.models import User
from banking.models.customer import Customer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models


class customerTransferForm(ModelForm):
    amount = DecimalField(max_digits=10, decimal_places=2)
    debit_account = ChoiceField(queryset=Customer.objects.none())
    debit_text = CharField(max_length=25)
    credit_account = IntegerField(max_digits = 10,label='The Credit Account Number')
    credit_text = CharField(max_length=25)

    def clean(self):
        super().clean()

        credit_account = self.cleaned_data.get('credit_account')

        try:
          Account  # mangler en account klasse (pk=credit_account)
        except #mangler fra view
            self.add_error('credit_account', 'The credit account couldnt be found.')
        amount = self.cleaned_data.get('amount')

        if amount < 0:
            self.add_error('amount', 'Amount cannot be a negative amount')
        return self.cleaned_data


