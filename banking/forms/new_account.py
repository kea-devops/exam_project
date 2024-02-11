from django.forms import ModelForm, CharField, EmailField, ChoiceField, PasswordInput
from banking.models.account import Account
from banking.models.account_type import Account_type


class AccountForm(ModelForm):
    def account_types():
        types = Account_type.objects.all()
        pairs = []
        for t in types:
            if not t.internal_use:
                pairs.append((t.name, f'{t.name} ({t.interest_rate}%)'))
        return tuple(pairs)


    name = CharField(max_length=30, required=True)
    account_type = ChoiceField(choices=account_types)
    
    class Meta:
        model = Account
        fields = ('name',)



    def __init__(self, *args, **kwargs):
        exclude_type = kwargs.pop('exclude_type', False)
        super(AccountForm, self).__init__(*args, **kwargs)

        if exclude_type:
            del self.fields['account_type']
