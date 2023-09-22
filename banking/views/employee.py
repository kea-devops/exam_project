from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from banking.forms.new_customer import CustomerForm
from banking.models.costumer_rank import Customer_rank
from banking.models.customer import Customer

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
    
    print(customers.values())

    context = { 'customers': customers, 'page': page+1, 'page_count': page_count+1 }

    return render(request, 'banking/employee/index.html', context)

@login_required
def customer(request):
    customer_form = CustomerForm()

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer = customer_form.instance
            group = Group.objects.get(name='customers')
            user = User(
                username=customer.email,
                email=customer.email,
                first_name=customer.first_name,
                last_name=customer.last_name,
                password=make_password(request.POST['password'])
            )
            user.save()
            user.groups.add(group)
            user.save()
            print(user.id)
            customer_form.instance.user_id = user
            customer_form.instance.customer_rank = Customer_rank.objects.get(name=request.POST['customer_rank'])
            customer_form.save()   
            return redirect('/employee')

    if not customer_form:
        customer_form = CustomerForm()

    context = { 'customer_form': customer_form }

    return render(request, 'banking/employee/customer.html', context)