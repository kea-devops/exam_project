# Generated by Django 5.0.2 on 2024-02-10 19:17

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Customer_rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('rank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='banking.customer_rank')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_num', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='banking.account_type')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='banking.customer')),
            ],
        ),
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending Loan'), ('approved_employee', 'Pending Supervisor Approval'), ('approved', 'Approved Loan'), ('denied', 'Denied Loan')], default='pending', max_length=20)),
                ('supervisor_approved', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='banking.account')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loan_applications', to='banking.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('counterparty', models.CharField(max_length=15)),
                ('type', models.CharField(choices=[('loan_deposit', 'Loan Deposit'), ('internal_transfer', 'Internal Transfer'), ('external_transfer', 'External Transfer'), ('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('payment', 'Payment'), ('fee', 'Fee'), ('interest', 'Interest')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='banking.account')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='banking.transaction')),
            ],
        ),
    ]
