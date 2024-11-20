from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from banking.models import CustomUser  # Adjust this import to your actual path

class Command(BaseCommand):
    help = 'Remove custom permissions for CustomUser model'

    def handle(self, *args, **options):
        # Get the ContentType for the CustomUser model
        custom_user_content_type = ContentType.objects.get_for_model(CustomUser)

        # Define the list of custom permission codenames you want to remove
        custom_permissions_to_remove = [
            'edit_atm_monthly_limit',
            'edit_mpin_mtpin',
            'edit_password',
            'edit_account',
            'edit_loan',
            'add_transactions',
            'view_account',
            'view_transactions',
            'view_loan',
            'view_installments',
            'view_atm_cards',
            'view_customer',
            'add_installments',
        ]

        # Filter the permissions for CustomUser content_type and with the specified codenames
        permissions_to_delete = Permission.objects.filter(
            content_type=custom_user_content_type, codename__in=custom_permissions_to_remove
        )

        # Delete the filtered permissions
        count_deleted = permissions_to_delete.delete()[0]  # delete() returns a tuple (count, dict)

        self.stdout.write(self.style.SUCCESS(f"Deleted {count_deleted} custom permissions for CustomUser."))
