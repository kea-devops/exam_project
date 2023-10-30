from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from banking.forms.new_loan_application import LoanApplicationForm
from banking.forms.new_customer import CustomerForm
from banking.models.account import Account, LoanApplication
from banking.models.ledger import Ledger, generate_balance
from banking.models.account_type import Account_type
from banking.forms.new_account import AccountForm
from banking.models.customer import Customer

@login_required
def index(request):
    customer = get_object_or_404(Customer, user=request.user)
    return redirect('banking:customer/detail', pk=customer.pk)

@login_required
def detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
       print("Inside if: ",request.method)
       form = CustomerForm(request.POST, instance=customer, exclude_password_rank=True)
       if form.is_valid():
          form.save()       
          return redirect('banking:customer/detail', pk=customer.pk)
    else:
       form = CustomerForm(instance=customer, exclude_password_rank=True)
    context = {'customer': customer, 'customer_form': form}
    return render(request, 'banking/customer/customer_detail.html', context)
    

def create_account(request):
    customer = Customer.objects.get(user=request.user)
    account_form = AccountForm()

    if request.method == 'POST':
       account_form = AccountForm(request.POST)
       if account_form.is_valid():
          account_type = get_object_or_404(Account_type, name=request.POST['account_type'])
          if request.POST['account_type'] == 'Loan' and customer.customer_rank.name not in ['Gold', 'Silver']:
             return HttpResponse('Only gold and silver ranked customers can apply for loans.')
          account_form.instance.customer = customer
          account_form.instance.account_type = account_type   
          account_form.save()
          return redirect(f'/customer/')

    context = {'customer': customer, 'account_form': account_form}
    return render(request, 'banking/customer/account.html', context)

@login_required
def loan_application_list(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    loan_applications = LoanApplication.objects.filter(customer=customer)
    if customer.customer_rank.name not in ['Gold', 'Silver']:
        return HttpResponse('Only gold and silver ranked customers can apply for loans.')
    if request.method == 'POST':
       loan_form = LoanApplicationForm(request.POST)
       if loan_form.is_valid():
           loan_application = loan_form.save(commit=False)
           loan_application.customer = customer
           loan_application.save()
           print("Loan application = ",loan_application)
    else:
       loan_form = LoanApplicationForm()

    context = {'customer': customer, 'loan_form': loan_form, 'loan_applications': loan_applications}
    return render(request, 'banking/customer/loan_application_list.html', context)

@login_required
def loans_list(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    loans = generate_balance(Account.objects.filter(account_type__name='Loan', customer=pk))

    context = { 'customer': customer, 'loans': loans }
    return render(request, 'banking/customer/loan_list.html', context)
   
