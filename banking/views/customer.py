from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from banking.models.customer import Customer
from banking.models.account import Account, LoanApplication
from banking.models.account_type import Account_type
from banking.forms.new_account import AccountForm
from banking.forms.new_loan_application import LoanApplicationForm
from django.contrib.auth.decorators import login_required


def index(request):
    customer = get_object_or_404(Customer, user_id=request.user)
    accounts = Account.objects.filter(customerid=customer).select_related('account_typeid')
    loan_applications = LoanApplication.objects.filter(customerid=customer)
    context = {'customer': customer, 'accounts': accounts, 'loan_applications': loan_applications}
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

def apply_loan(request):
    customer = get_object_or_404(Customer, user_id=request.user)
    if customer.customer_rank.name not in ['Gold', 'Silver']:
        return HttpResponse('Only gold and silver ranked customers can apply for loans. <a href="/customer/account/">Go back</a>')
    if request.method == 'POST':
       loan_form = LoanApplicationForm(request.POST)
       if loan_form.is_valid():
           loan_application = loan_form.save(commit=False)
           loan_application.customerid = customer
           loan_application.save()
           return redirect('banking:customer')
    else:
       loan_form = LoanApplicationForm()

    context = {'customer': customer, 'loan_form': loan_form}
    return render(request, 'banking/customer/apply_loan.html', context)
