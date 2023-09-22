from django.urls import path
from .views import index


app_name = 'banking'

urlpatterns = [
    path('', index.index, name='index'),
]