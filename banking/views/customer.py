from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from banking.models.customer import Customer
from banking.models.account import Account
from banking.models.account_type import Account_type
from banking.forms.new_account import AccountForm
from django.contrib.auth.decorators import login_required


def index(request):
    customer = get_object_or_404(Customer, user_id=request.user)
    accounts = Account.objects.filter(customerid=customer).select_related('account_typeid')
    context = {'customer': customer, 'accounts': accounts}
    return render(request, 'banking/customer/index.html', context)
    

def create_account(request):
    customer = Customer.objects.get(user_id=request.user)
    account_form = AccountForm()

    if request.method == 'POST':
       account_form = AccountForm(request.POST)
       if account_form.is_valid():
          account_type = get_object_or_404(Account_type, name=request.POST['account_type'])
          if request.POST['account_type'] == 'Loan' and customer.customer_rank.name not in ['Gold', 'Silver']:
             return HttpResponse('Only gold and silver ranked customers can apply for loans. <a href="/customer/account/">Go back</a>')
          account_form.instance.customerid = customer
          account_form.instance.account_typeid = account_type   
          account_form.save()
          return redirect(f'/customer/')

    context = {'customer': customer, 'account_form': account_form}
    return render(request, 'banking/customer/account.html', context)
