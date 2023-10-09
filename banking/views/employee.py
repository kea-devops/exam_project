from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db.models import Sum
from banking.forms.new_customer import CustomerForm
from banking.forms.new_account import AccountForm
from banking.models.costumer_rank import Customer_rank
from banking.models.customer import Customer
from banking.models.account import Account
from banking.models.account_type import Account_type
from banking.models.ledger import Ledger

@login_required
def index(request):

    page = request.GET.get('page', '1')
    if page.isdigit() and int(page) > 0:
        page = int(page)
    else:
        page = 1
    
    customer_count = Customer.objects.all().count()
    page_count = customer_count // 10
    if page > page_count:
        page = page_count

    customers = Customer.objects.all().select_related('user_id', 'customer_rank')[(page)*10:(page)*10+10]

    context = { 'customers': customers, 'page': page+1, 'page_count': page_count+1 }

    return render(request, 'banking/employee/index.html', context)

@login_required
def customer(request):
    customer_form = CustomerForm()

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer = customer_form.instance
            user = User(
                username=customer.email,
                email=customer.email,
                first_name=customer.first_name,
                last_name=customer.last_name,
                password=make_password(request.POST['password'])
            )
            user.save()

            customer_form.instance.user_id = user
            customer_form.instance.customer_rank = Customer_rank.objects.get(name=request.POST['customer_rank'])
            customer_form.save()   
            return redirect('/employee')

    if not customer_form:
        customer_form = CustomerForm()

    context = { 'customer_form': customer_form }

    return render(request, 'banking/employee/customer.html', context)

@login_required
def customer_details(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'PATCH':
        rank = request.PATCH['rank']
        rank = get_object_or_404(Customer_rank, name=rank)
        customer.customer_rank = rank
        customer.save()
        return HttpResponse(f'Customer Rank: {rank.name}')


    ranks = Customer_rank.objects.all()
    accounts = Account.objects.filter(customerid=customer).select_related('account_typeid')
    for account in accounts:
        balance = Ledger.objects.filter(customer_id=customer).aggregate(Sum('amount'))['amount__sum']
        if balance is None:
            account.balance = 0
        else:
            account.balance = balance
        account.balance = '{0:.2f}'.format(account.balance)

    context = { 'customer': customer, 'accounts': accounts, 'ranks': ranks }

    return render(request, 'banking/employee/customer_details.html', context)

@login_required
def customer_account(request, pk):
    account_form = AccountForm()

    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_type = get_object_or_404(Account_type, name=request.POST['account_type'])
            account_form.instance.customerid = customer
            account_form.instance.account_typeid = account_type
            account_form.save()   
            return redirect(f'/employee/customer/{pk}')

    context = { 'customer': customer, 'account_form': account_form }
    return render(request, 'banking/employee/account.html', context)