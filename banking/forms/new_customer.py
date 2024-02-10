from django.forms import ModelForm, CharField, EmailField, ChoiceField, PasswordInput
from django.contrib.auth.models import User
from banking.models.customer import Customer


class CustomerForm(ModelForm):
    first_name = CharField(max_length=50, required=True)
    last_name = CharField(max_length=50, required=True)
    email = EmailField(max_length=100, required=True)
    phone = CharField(max_length=20, required=True)
    rank = ChoiceField(choices=(
        ('Blue', 'Blue'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold')
    ))
    password = CharField(max_length=64, widget=PasswordInput)
    re_password = CharField(max_length=64, widget=PasswordInput)
    
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone')

    def save(self, commit=True):
        instance = super(CustomerForm, self).save(commit=False)

        user = instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.save()

        if commit:
            instance.save()

        return instance


    def __init__(self, *args, **kwargs):
        exclude_password_rank = kwargs.pop('exclude_password_rank', False)
        super(CustomerForm, self).__init__(*args, **kwargs)

        if exclude_password_rank:
            del self.fields['password']
            del self.fields['re_password']
            del self.fields['rank']
