from django.core.management.base import BaseCommand
from banking.models import *
from banking.signals import (
    create_employee_credentials,
    create_customer_credentials,
    create_custom_user_from_employee_credentials,
    create_custom_user_from_customer_credentials,
)

class Command(BaseCommand):
    help = 'Create employee and customer credentials in the specified order'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Creating employees...'))
        self.create_employees()

        self.stdout.write(self.style.NOTICE('Creating employee credentials...'))
        self.create_employee_credentials()

        self.stdout.write(self.style.NOTICE('Creating CustomUser instances for employees...'))
        self.create_custom_users_for_employees()

        self.stdout.write(self.style.NOTICE('Creating customers...'))
        self.create_customers()

        self.stdout.write(self.style.NOTICE('Creating customer credentials...'))
        self.create_customer_credentials()

        self.stdout.write(self.style.NOTICE('Creating CustomUser instances for customers...'))
        self.create_custom_users_for_customers()

        self.stdout.write(self.style.SUCCESS('All credentials and users created successfully!'))

    def create_employees(self):
        # Logic to create employees if needed, or just retrieve existing employees
        pass  # Implement if necessary; if not, remove this method

    def create_employee_credentials(self):
        employees_without_credentials = employee.objects.exclude(
            employee_credentials_by_employee_id__isnull=False
        )
        for emp in employees_without_credentials:
            create_employee_credentials(sender=employee, instance=emp, created=True)

    def create_custom_users_for_employees(self):
        for emp_cred in employee_credentials.objects.all():
            create_custom_user_from_employee_credentials(sender=employee_credentials, instance=emp_cred, created=True)

    def create_customers(self):
        # Logic to create customers if needed, or just retrieve existing customers
        pass  # Implement if necessary; if not, remove this method

    def create_customer_credentials(self):
        customers_without_credentials = customer.objects.exclude(
            customer_credentials_by_cin__isnull=False
        )
        for cust in customers_without_credentials:
            create_customer_credentials(sender=customer, instance=cust, created=True)

    def create_custom_users_for_customers(self):
        for cust_cred in customer_credentials.objects.all():
            create_custom_user_from_customer_credentials(sender=customer_credentials, instance=cust_cred, created=True)
