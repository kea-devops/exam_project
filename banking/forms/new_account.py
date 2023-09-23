from django.forms import ModelForm, CharField, EmailField, ChoiceField, PasswordInput
from banking.models.account import Account
from banking.models.account_type import Account_type


class AccountForm(ModelForm):
    def account_types():
        types = Account_type.objects.all()
        pairs = []
        for t in types:
            
            pairs.append((t.name, f'{t.name} ({t.interest_rate}%)'))
        return tuple(pairs)


    name = CharField(max_length=30, required=True)
    account_type = ChoiceField(choices=account_types)
    
    class Meta:
        model = Account
        fields = ('name',)