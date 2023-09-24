from django.shortcuts import render, redirect, get_object_or_404
from banking.models.customer import Customer
from banking.models.account import Account
from banking.forms.new_account import AccountForm
from django.contrib.auth.decorators import login_required


def index(request):
    try:
        customer = Customer.objects.get(user_id=request.user)
        accounts = Account.objects.filter(customerid=customer).select_related('account_typeid')

        context = {'customer': customer, 'accounts': accounts}
        return render(request, 'banking/customer/index.html', context)
    except Customer.DoesNotExist:
        return HttpResponse('You are not a customer.')
