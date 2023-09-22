from django.forms import ModelForm, CharField, EmailField, ChoiceField, PasswordInput
from django.contrib.auth.models import User
from banking.models.customer import Customer


class CustomerForm(ModelForm):
    first_name = CharField(max_length=50, required=True)
    last_name = CharField(max_length=50, required=True)
    email = EmailField(max_length=100, required=True)
    phone = CharField(max_length=20, required=True)
    customer_rank = ChoiceField(choices=(
        ('Blue', 'Blue'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold')
    ))
    password = CharField(max_length=64, widget=PasswordInput)
    re_password = CharField(max_length=64, widget=PasswordInput)
    
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone')