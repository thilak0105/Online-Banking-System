# Create a management command in bank/management/commands/create_permissions.py
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from banking.models import CustomUser  # Adjust this import based on where your model is located

class Command(BaseCommand):
    help = 'Create custom permissions'

    def handle(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(CustomUser)  # Get the content type for CustomUser

        permissions = [
            ('view_account', 'Can View Account'),
            ('view_transactions', 'Can View Transactions'),
            ('view_loan', 'Can View Loan'),
            ('view_installments', 'Can View Installments'),
            ('view_atm_cards', 'Can View ATM Cards'),
            ('view_customer', 'Can View Customer Info'),
            ('add_transactions', 'Can Create Transactions'),
            ('add_installments', 'Can Create Loan Installments'),
            ('edit_atm_monthly_limit', 'Can Edit Monthly Limit for ATM Card'),
            ('edit_mpin_mtpin', 'Can Edit MPIN and MTPIN'),
            ('edit_password', 'Can Change Password'),
            ('edit_account', 'Can Alter Account'),
            ('edit_loan', 'Can Alter Loan'),
        ]

        for codename, name in permissions:
            # Create permission with the specified content type
            Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type  # Specify the content type
            )
            self.stdout.write(self.style.SUCCESS(f'Permission "{name}" created or already exists.'))