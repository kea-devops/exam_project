from django.urls import path
from .views import index, employee, customer


app_name = 'banking'

urlpatterns = [
    path('', index.index, name='index'),
    path('customer/', customer.index, name='customer'),
    path('customer/account/', customer.create_account, name='customer/account'),
    path('customer/apply_loan/', customer.apply_loan, name='customer/apply_loan'),
    path('employee/', employee.index, name='employee'),
    path('employee/customer', employee.customer, name='employee/customer'),
    path('employee/customer/<int:pk>', employee.customer_details, name='employee/customer_pk'),
    path('employee/customer/<int:pk>/account', employee.customer_account, name='employee/customer/account'),
]
