from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission

class Command(BaseCommand):
    help = 'Deletes duplicate permissions'

    def handle(self, *args, **options):
        duplicate_codenames = [
            "add_transactions",
            "view_account",
            "view_installments",
            "view_transactions",
            "view_atm_cards",
            "view_customer",
            "view_loan",
            "add_installments",
        ]

        for codename in duplicate_codenames:
            duplicate_permissions = Permission.objects.filter(codename=codename)
            if duplicate_permissions.count() > 1:
                # Keep the first one and delete the others
                for perm in duplicate_permissions[1:]:
                    self.stdout.write(f"Deleting duplicate permission: {perm.name}")
                    perm.delete()
        self.stdout.write("Duplicate permissions removed successfully.")