from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q, Sum
from django.conf import settings
from banking.models.account import Account
from banking.models.customer import Customer
from banking.forms.new_account import AccountForm
from banking.forms.new_customer import CustomerForm
from banking.forms.new_transaction import TransactionForm, TransactionError
from banking.models.ledger import Ledger, get_balances
from banking.models.loan_application import LoanApplication
from banking.forms.new_loan_application import LoanApplicationForm

@login_required
def index(request):
    customer = get_object_or_404(Customer, user=request.user)
    return redirect('banking:customer/detail', pk=customer.pk)

@login_required
def detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'PATCH':
       form = CustomerForm(request.PATCH, instance=customer, exclude_password_rank=True)
       if form.is_valid():
          customer = form.save()       
    
    customer_form = CustomerForm(instance=customer, exclude_password_rank=True)
    transaction_form = TransactionForm(customer)
    context = {'customer': customer, 'customer_form': customer_form, 'transaction_form': transaction_form}
    return render(request, 'banking/customer/customer_detail.html', context)
    
@login_required
def account_list(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    accounts = get_balances(Account.objects.filter(~Q(account_type__name='Loan'), customer=pk))
    context = {'customer': customer, 'accounts': accounts}
    return render(request, 'banking/customer/account_list.html', context)

@login_required
def account_details(request, customer_pk, account_pk):
    customer = get_object_or_404(Customer, pk=customer_pk)
    account = get_balances([get_object_or_404(Account, pk=account_pk)])[0]
    movements = Ledger.objects.filter(account=account).order_by('-created_at')
    bank_reg = getattr(settings, 'BANK_REG_NUM', None)

    if request.method == 'PATCH':
       form = AccountForm(request.PATCH, instance=account, exclude_type=True)
       if form.is_valid():
          account.name = form.cleaned_data['name']
          account.save()
    else:
       form = AccountForm(instance=account, exclude_type=True)
    
    context = {'customer': customer, 'account': account, 'form': form, 'movements': movements, 'bank_reg': bank_reg}
    return render(request, 'banking/customer/account_details.html', context)

@login_required
def loan_application_list(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    loan_applications = LoanApplication.objects.filter(customer=customer)

    if request.method == 'POST':
       if customer.rank.score < 25:
           # return 403
           return HttpResponse('You do not qualify for a loan.', status=403)
       loan_form = LoanApplicationForm(customer, request.POST)
       if loan_form.is_valid():
           loan_application = loan_form.save(commit=False)
           account = Account.objects.get(pk=request.POST.get('account'))
           loan_application.account = account
           loan_application.customer = customer
           loan_application.save()
    else:
       loan_form = LoanApplicationForm(customer)

    context = {'customer': customer, 'loan_form': loan_form, 'loan_applications': loan_applications}
    return render(request, 'banking/customer/loan_application_list.html', context)

@login_required
def loans_list(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    loans = get_balances(Account.objects.filter(account_type__name='Loan', customer=pk))
    print("Loans = ", loans)
    context = { 'customer': customer, 'loans': loans }
    return render(request, 'banking/customer/loan_list.html', context)
   

@login_required
def account_movements(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    if account.customer.user != request.user:
        return HttpResponse('Unauthorized', status=401)

    movements = Ledger.objects.filter(account=account).order_by('-created_at')
    balance = movements.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'account': account,
        'movements': movements,
        'balance': balance,
    }
    return render(request, 'banking/customer/account_movements.html', context)

@login_required
def transaction_list(request, customer_pk):
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)
    
    user = request.user
    customer = get_object_or_404(Customer, pk=customer_pk)
    transaction = TransactionForm(customer, request.POST)
    if transaction.is_valid():
        try:
            account_pk = transaction.process(user)
        except TransactionError as e:
            return HttpResponse(str(e.message), status=e.status_code)
    
    return redirect('banking:customer/account', customer_pk=customer_pk, account_pk=account_pk)
