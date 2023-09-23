def populate_models(sender, **kwargs):
    from django.contrib.auth.models import User, Group
    from django.contrib.auth.hashers import make_password
    from banking.models.costumer_rank import Customer_rank
    from banking.models.account_type import Account_type
    from decimal import Decimal

    # Create customer and employee groups if not exists
    employee_group, _ = Group.objects.get_or_create(name='employees')
    Group.objects.get_or_create(name='customers')
    
    # Create admin if not exists and add to employee group
    admin, created = User.objects.get_or_create(username='admin')
    if created:
        admin.is_staff = True
        admin.is_superuser = True
        admin.groups.add(employee_group)
        admin.password = make_password('123456')
        admin.save()

    Customer_rank.objects.get_or_create(name='Blue')
    Customer_rank.objects.get_or_create(name='Silver')
    Customer_rank.objects.get_or_create(name='Gold')

    Account_type.objects.get_or_create(name='Regular', interest_rate=Decimal(2.10))
    Account_type.objects.get_or_create(name='Savings', interest_rate=Decimal(5.75))
    Account_type.objects.get_or_create(name='Loan', interest_rate=Decimal(12.32))
