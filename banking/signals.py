from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import customer_credentials, CustomUser
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from .models import CustomUser


@receiver(post_save, sender=customer_credentials)
def create_custom_user(sender, instance, created, **kwargs):
    if created:
        user = CustomUser.objects.create(
            user_id=instance.user_id,
        )
        user.set_password(instance.password)
        user.save()

from .models import customer, customer_credentials
import random
import string

def generate_random_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_pin(length=4):
    return ''.join(random.choices(string.digits, k=length))

@receiver(post_save, sender=customer)
def create_customer_credentials(sender, instance, created, **kwargs):
    if created:
        user_id = f"user_{instance.cin}" 

        password = generate_random_password()
        mpin = generate_pin()
        mtpin = generate_pin()

        phone_id = instance.phone

        customer_credentials.objects.create(
            user_id=user_id,
            password=password,
            mpin=mpin,
            mtpin=mtpin,
            cin_id=instance.cin,
            phone_id=phone_id,
        )


@receiver(post_save, sender=customer_credentials)
def create_custom_user_from_customer_credentials(sender, instance, created, **kwargs):
    if created:
        if not CustomUser.objects.filter(user_id=instance.user_id).exists():
            # Create the CustomUser instance
            user = CustomUser.objects.create(
                user_id=instance.user_id,
                password=make_password(instance.password),  # Hash the password
                is_active=True,  # Set as active
                is_staff=False,  # Not a staff user
            )
            # Add the user to the 'customer' group
            customer_group, _ = Group.objects.get_or_create(name='customer')
            user.groups.add(customer_group)
            print(f"User {instance.user_id} created from customer credentials and added to customer group.")
        else:
            print(f"User {instance.user_id} already exists.")



from .models import employee, employee_credentials

@receiver(post_save, sender=employee)
def create_employee_credentials(sender, instance, created, **kwargs):
    if created:
        # Generate employee user_id using employee_id or other details
        user_id = f"emp_{instance.employee_id}"

        # Generate a random password
        password = generate_random_password()

        # Create the employee credentials
        employee_credentials.objects.create(
            employee_id=instance,  # ForeignKey to employee
            user_id=user_id,       # Generated user ID
            password=password,     # Generated password
            phone=instance         # Phone number from employee
        )


from django.contrib.auth.hashers import make_password
from .models import employee_credentials, CustomUser

@receiver(post_save, sender=employee_credentials)
def create_custom_user_from_employee_credentials(sender, instance, created, **kwargs):
    if created:
        if not CustomUser.objects.filter(user_id=instance.user_id).exists():
            # Create the CustomUser instance and mark as staff
            user = CustomUser.objects.create(
                user_id=instance.user_id,
                password=make_password(instance.password),  # Hash the password
                is_active=True,  # Set as active
                is_staff=True,   # Mark as staff
            )
            # Add the user to the 'staff' group
            staff_group, _ = Group.objects.get_or_create(name='staff')
            user.groups.add(staff_group)
            print(f"User {instance.user_id} created from employee credentials and added to staff group.")
        else:
            print(f"User {instance.user_id} already exists.")


from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import CustomUser


from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def assign_permissions_to_groups(sender, **kwargs):
    if sender.name == 'bank':  # Ensure this runs only for your 'bank' app
        # Create or get the groups
        customer_group, created = Group.objects.get_or_create(name='customer')
        staff_group, created = Group.objects.get_or_create(name='staff')

        # Define customer permissions
        customer_permissions = [
            'bank.view_account',
            'bank.view_transactions',
            'bank.view_loan',
            'bank.view_installments',
            'bank.view_atm_cards',
            'bank.view_customer_info',
            'bank.add_transactions',
            'bank.add_installments',
            'bank.edit_atm_monthly_limit',
            'bank.edit_mpin_mtpin',
            'bank.edit_password'
        ]

        # Assign customer permissions to customer group
        for perm in customer_permissions:
            try:
                permission = Permission.objects.get(codename=perm.split('.')[1])  # Extract the codename
                customer_group.permissions.add(permission)
            except Permission.DoesNotExist:
                print(f"Permission '{perm}' does not exist.")

        # Define staff permissions (includes customer permissions + staff-specific permissions)
        staff_permissions = customer_permissions + [
            'bank.edit_account',
            'bank.edit_loan',
            # Add any additional staff permissions here
        ]

        # Assign staff permissions to staff group
        for perm in staff_permissions:
            try:
                permission = Permission.objects.get(codename=perm.split('.')[1])
                staff_group.permissions.add(permission)
            except Permission.DoesNotExist:
                print(f"Permission '{perm}' does not exist.")

        print("Permissions assigned to customer and staff groups.")


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import loan
from datetime import date

@receiver(post_save, sender=loan)
def update_loan_status(sender, instance, **kwargs):
    # Get today's date
    today = date.today()

    # Check if next_inst_date is today or before
    if instance.next_inst_date <= today and instance.loan_status != 'P':
        # Update loan status to 'P' (Pending Due)
        instance.loan_status = 'P'
        instance.save(update_fields=['loan_status'])
        print(f"Loan {instance.loan_id} status updated to 'P' (Pending Due).")


