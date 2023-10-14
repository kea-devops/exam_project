from django.urls import path
from .views import index, employee, customer


app_name = 'banking'

urlpatterns = [
    path('', index.index, name='index'),
    path('customer/', customer.index, name='customer'),
    path('customer/account/', customer.create_account, name='customer/account'),
    path('customer/apply_loan/', customer.apply_loan, name='customer/apply_loan'),
    path('employee/', employee.index, name='employee'),
    path('employee/customers', employee.customer_list, name='employee/customers'),
    path('employee/customers/<int:pk>', employee.customer_details, name='employee/customer'),
    path('employee/customers/<int:customer_pk>/loans', employee.loan_list, name='employee/loans'),
    path('employee/customers/<int:customer_pk>/loans/<int:loan_pk>', employee.account_list, name='employee/loan'),
    path('employee/customers/<int:customer_pk>/accounts', employee.account_list, name='employee/accounts'),
    path('employee/customers/<int:customer_pk>/accounts/<int:account_pk>', employee.account_details, name='employee/account'),
    path('employee/customers/<int:customer_pk>/loan_applications', employee.loan_application_list, name='employee/loan_applications'),
    path('employee/customers/<int:customer_pk>/loan_applications/<int:application_pk>', employee.loan_application_details, name='employee/loan_application'),
]
