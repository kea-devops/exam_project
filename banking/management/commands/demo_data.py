from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password        
from django.contrib.auth.models import User
from banking.models.customer import Customer
from banking.models.customer_rank import Customer_rank
from django.db.models import DateTimeField

# Demo Customers
user1 = User(username="bob@johnson.com", email="bob@johnson.com", first_name="Bob", last_name="Johnson", password=make_password("123456"))
customer1 = Customer(user = user1, rank = Customer_rank.objects.get(name="Blue"), first_name = user1.first_name, last_name = user1.last_name, email = user1.email, phone = "12345678", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True),)
user2 = User(username="john@bobson.com", email="john@bobson.com", first_name="John", last_name="Bobson", password=make_password("123456"))
customer2 = Customer(user = user2, rank = Customer_rank.objects.get(name="Silver"), first_name = user2.first_name, last_name = user2.last_name, email = user2.email, phone = "87654321", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True),)
user3 = User(username="jane@johnson.com", email="jane@johnson.com", first_name="Jane", last_name="Johnson", password=make_password("123456"))
customer3 = Customer(user = user3, rank = Customer_rank.objects.get(name="Gold"),first_name = user3.first_name, last_name = user3.last_name,email = user3.email, phone = "12348765", created_at = DateTimeField(auto_now_add=True), updated_at = DateTimeField(auto_now=True),)

class Command(BaseCommand):
    def handle(self, **options):
        user1.save()
        customer1.save()
        user2.save()
        customer2.save()
        user3.save()
        customer3.save()
        print("Demo data created successfully")
        