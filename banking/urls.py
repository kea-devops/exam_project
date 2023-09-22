from django.urls import path
from .views import index, employee


app_name = 'banking'

urlpatterns = [
    path('', index.index, name='index'),
    path('employee/', employee.index, name='employee'),
    path('employee/customer', employee.customer, name='employee/customer'),
]
