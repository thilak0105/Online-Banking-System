from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from datetime import date
from django.utils import timezone # DO NOT REMOVE!
from decimal import Decimal
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal


class employee(models.Model):
    employee_id = models.BigIntegerField(primary_key=True, validators=[MaxValueValidator(999999), MinValueValidator(100000)],editable=False,)
    def save(self, *args, **kwargs):
        if not self.employee_id:  
            last_account = employee.objects.order_by('-employee_id').first()
            if last_account:
                self.employee_id = last_account.employee_id + 1
            else:
                self.employee_id = 100001
        super().save(*args, **kwargs)

    fname = models.CharField(max_length=255, null=False)
    lname = models.CharField(max_length=255, null=True, blank=True)
    
    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDERS, default='M')
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.BigIntegerField(null=False, blank=False, unique=True, default=9999999999, validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)])
    date_of_birth = models.DateField()
    door_no = models.CharField(max_length=20, null=False, default='None')
    street_name = models.CharField(max_length=255, null=False, default='None')
    city = models.CharField(max_length=255, null=False, default='None')
    pin_code = models.IntegerField(validators=[MaxValueValidator(999999), MinValueValidator(100000)], null=False, default=100000)
    pan_no = models.CharField(max_length=10, null=True, unique=True, validators=[MinLengthValidator(10)])
    designation = models.CharField(max_length=255, null=False, default='employee')
    branch = models.CharField(max_length=255, null=False, default='main')
    
    def __str__(self):
        if self.gender == 'M':
            if self.lname:
                return f"Mr. {self.fname} {self.lname}"
            return f"Mr. {self.fname}"
        elif self.gender == 'F':
            if self.lname:
                return f"Ms. {self.fname} {self.lname}"
            return f"Ms. {self.fname}"
        if self.lname:
            return f"{self.fname} {self.lname}"
        return f"{self.fname}"

class customer(models.Model):
    cin = models.BigIntegerField(unique=True, primary_key=True,blank=True,editable=False)

    def save(self, *args, **kwargs):
        if not self.cin:  
            last_account = customer.objects.order_by('-cin').first()
            if last_account:
                self.cin = last_account.cin + 1
            else:
                self.cin = 10000000
        super().save(*args, **kwargs)

    fname = models.CharField(max_length=255, null=False)
    lname = models.CharField(max_length=255, null=True, blank=True)
    
    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDERS, default='M')
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.BigIntegerField(null=False, blank=False, unique=True, default=9999999999, validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)])
    date_of_birth = models.DateField()
    door_no = models.CharField(max_length=20, null=False, default='None')
    street_name = models.CharField(max_length=255, null=False, default='None')
    city = models.CharField(max_length=255, null=False, default='None')
    pin_code = models.IntegerField(validators=[MaxValueValidator(999999), MinValueValidator(100000)], null=False, default=100000)
    pan_no = models.CharField(max_length=10, null=True, unique=True, validators=[MinLengthValidator(10)])
    managed_by=models.ForeignKey(employee,on_delete=models.CASCADE,to_field='employee_id',related_name='Staff_in_charge',null=False,default=100000) # type: ignore
    def __str__(self):
        if self.gender == 'M':
            if self.lname:
                return f"Mr. {self.fname} {self.lname}"
            return f"Mr. {self.fname}"
        elif self.gender == 'F':
            if self.lname:
                return f"Ms. {self.fname} {self.lname}"
            return f"Ms. {self.fname}"
        if self.lname:
            return f"{self.fname} {self.lname}"
        return f"{self.fname}"


class account(models.Model):
    acc_no = models.BigIntegerField(unique=True, primary_key=True,blank=True,editable=False,)
    def save(self, *args, **kwargs):
        if not self.acc_no:  # This ensures the acc_no is only set automatically
            last_account = account.objects.order_by('-acc_no').first()
            if last_account:
                self.acc_no = last_account.acc_no + 1
            else:
                self.acc_no = 1000000000  # Start from a 10-digit number
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.acc_no)

    ifsc = models.CharField(max_length=11, null=False, default='YOURBANK001', validators=[MinLengthValidator(11)])

    ACCOUNT_TYPES = [
        ('SB', 'Savings Account'),
        ('CA', 'Current Account'),
        ('SA', 'Salary Account'),
        ('FD', 'Fixed Deposit Account')
    ]
    acc_type = models.CharField(max_length=2, choices=ACCOUNT_TYPES, default='SB', null=False, blank=False)

    ACCOUNT_STATUS = [
        ('F', 'FROZEN Account'),
        ('A', 'ACTIVE Account'),
        ('L', 'LOW BALANCE Account'),
    ]
    acc_status = models.CharField(max_length=1, choices=ACCOUNT_STATUS, null=False, blank=False,default='A')
    remarks = models.TextField(max_length=1000, null=False, default='No remarks')
    date_of_opening = models.DateTimeField(auto_now_add=True,null=False,editable=False,)
    cin = models.ForeignKey(customer, on_delete=models.CASCADE, to_field='cin', related_name='accounts_by_cin',)
    acc_balance = models.BigIntegerField(null=False, default=0)
    min_balance = models.BigIntegerField(null=False, default=0)


class atm_cards(models.Model):
    card_no = models.BigIntegerField(primary_key=True, validators=[MaxValueValidator(9999999999999999), MinValueValidator(1000000000000000)], default=1111222233334444,editable=False,)
    acc_no = models.ForeignKey(account, on_delete=models.CASCADE, to_field='acc_no')

    CARD_TYPES = [
        ('B', 'Basic'),
        ('P', 'Platinum'),
        ('E', 'Elite')
    ]
    card_type = models.CharField(max_length=1, choices=CARD_TYPES, default='B', null=False)

    CRED_DEB = [
        ('D', 'DEBIT'),
        ('C', 'CREDIT')
    ]
    cred_debt = models.CharField(max_length=1, choices=CRED_DEB, default='D', null=False) # is it a CREDIT OR DEBIT CARD?
    monthly_limit = models.BigIntegerField(null=False, default=25000)
    exp_date = models.DateField()
    cvv = models.IntegerField(validators=[MaxValueValidator(999), MinValueValidator(100)], default=111, null=False,editable=False,)
    issue_date = models.DateField(default=date.today)


class acc_atm_cards(models.Model):
    card_no = models.ForeignKey(atm_cards, on_delete=models.CASCADE, to_field='card_no')
    phone = models.ForeignKey(customer, on_delete=models.CASCADE, to_field='phone', related_name='atm_cards_by_phone')


class transactions(models.Model):
    trans_id = models.BigIntegerField(unique=True, primary_key=True,blank = True,verbose_name='Transaction ID',editable=False)

    def save(self, *args, **kwargs):
        if not self.trans_id:  # This ensures the trans_id is only set automatically
            last_transaction = transactions.objects.order_by('-trans_id').first()
            if last_transaction:
                self.trans_id = last_transaction.trans_id + 1
            else:
                self.trans_id = 100000000000000  # Start from a 15-digit number
        super().save(*args, **kwargs)

    trans_time = models.DateTimeField(auto_now_add=True,null=False,blank=False,verbose_name='Transaction Time',editable=False)
    from_acc = models.ForeignKey(account, on_delete=models.CASCADE, to_field='acc_no', related_name='transactions_from_account',verbose_name='From Account',editable=False)
    to_acc = models.ForeignKey(account, on_delete=models.CASCADE, to_field='acc_no', related_name='transactions_to_account',verbose_name='To Account',editable=False)
    trans_amt = models.DecimalField(null=False, default=1,max_digits=10,decimal_places=2,verbose_name='Transaction Amount',editable=False) # type: ignore

    TRAN_STATUS = [
        ('S', 'SUCCESS'),
        ('F', 'FAILED')
    ]
    trans_status = models.CharField(max_length=1, choices=TRAN_STATUS, default='S', null=False,verbose_name="Status")
    remarks = models.TextField(max_length=1000,null=False, default='No remarks',verbose_name='Remarks')
    def __str__(self):
        return str(self.trans_id)

class loan(models.Model):
    loan_id = models.BigIntegerField(unique=True, primary_key=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.loan_id:
            last_loan = loan.objects.order_by('-loan_id').first()
            if last_loan:
                self.loan_id = last_loan.loan_id + 1
            else:
                self.loan_id = 1000000000  # Start from a 10-digit number

        self.loan_amt += Decimal(self.loan_amt) * (self.interest / 100)
        self.due_amt = self.loan_amt // 12

        if not self.next_inst_date:
            self.next_inst_date = self.loan_issue_date + relativedelta(months=1)
        
        super().save(*args, **kwargs)

    customer = models.ForeignKey('customer', on_delete=models.CASCADE, to_field='cin', related_name='customer_loan', default=12345678) # type: ignore
    loan_issue_date = models.DateField(default=date.today, editable=False)
    loan_amt = models.BigIntegerField(null=False, default=1)
    interest = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=Decimal('7.00'))
    next_inst_date = models.DateField(blank=True)  # Auto-updated based on installment payment
    loan_end_date = models.DateField(default=date.today)
    
    LOAN_STAT = [
        ('A', 'ACTIVE'),
        ('P', 'PENDING DUE'),
        ('C', 'COMPLETED')
    ]
    loan_status = models.CharField(max_length=1, choices=LOAN_STAT, default='A', null=False)
    due_amt = models.BigIntegerField(null=False, default=0,blank=True)

    def __str__(self):
        return str(self.loan_id)


class installments(models.Model):
    installment_id = models.BigIntegerField(unique=True, primary_key=True,blank = True,verbose_name='Transaction ID',editable=False)

    def save(self, *args, **kwargs):
        if not self.installment_id:  # This ensures the trans_id is only set automatically
            last_transaction = installments.objects.order_by('-installment_id').first()
            if last_transaction:
                self.installment_id = last_transaction.installment_id + 1
            else:
                self.installment_id = 111111 
        super().save(*args, **kwargs)

    #installment_id = models.BigIntegerField(primary_key=True, default=111111)
    loan_id = models.ForeignKey(loan, on_delete=models.CASCADE, to_field='loan_id')
    installment_time = models.DateTimeField(auto_now_add=True,editable=False)
    installment_amt = models.DecimalField(null=False, default=1,max_digits=10,decimal_places=2,editable=False) # type: ignore
    def __str__(self):
        return str(self.installment_id)

class customer_credentials(models.Model):
    cin = models.ForeignKey(customer, on_delete=models.CASCADE, to_field='cin', related_name='customer_credentials_by_cin')
    mtpin = models.IntegerField(null=False, default=1111, validators=[MaxValueValidator(9999), MinValueValidator(9999)])
    mpin = models.IntegerField(null=False, default=1111, validators=[MaxValueValidator(9999), MinValueValidator(9999)])
    user_id = models.CharField(primary_key=True, default='user01', max_length=100)
    password = models.CharField(max_length=15, null=False, default='user01')
    phone = models.ForeignKey(customer, on_delete=models.CASCADE, to_field='phone', related_name='customer_credentials_by_phone')
    def __str__(self):
        return self.user_id

class employee_credentials(models.Model):
    employee_id = models.ForeignKey(employee, on_delete=models.CASCADE, to_field='employee_id', related_name='employee_credentials_by_employee_id')
    user_id = models.CharField(primary_key=True, default='user01', max_length=100)
    password = models.CharField(max_length=15, null=False, default='user01')
    phone = models.ForeignKey(employee, on_delete=models.CASCADE, to_field='phone', related_name='employee_credentials_by_phone')
    def __str__(self):
        return self.user_id


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The User ID must be set')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(user_id, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):  # Inherit from PermissionsMixin for permissions
    user_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)  # Use default=timezone.now if you want it to auto-set

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            # View Permissions for Customers
            

            # Create Permissions for Customers

            # Update Permissions for Customers
            ('edit_atm_monthly_limit', 'Can Edit Monthly Limit for ATM Card'),
            ('edit_mpin_mtpin', 'Can Edit MPIN and MTPIN'),
            ('edit_password', 'Can Change Password'),

            # Edit Permissions for Staff
            ('edit_account', 'Can Alter Account'),
            ('edit_loan', 'Can Alter Loan'),

            # CONFLICTORSSSSS GO AWAAYYYY

            # ('add_transactions', 'Can Create Transactions'),
            # ('view_account', 'Can View Account'),
            # ('view_transactions', 'Can View Transactions'),
            # ('view_loan', 'Can View Loan'),
            # ('view_installments', 'Can View Installments'),
            # ('view_atm_cards', 'Can View ATM Cards'),
            # ('view_customer', 'Can View Customer Info'),
            # ('add_installments', 'Can Create Loan Installments'),

        ]

    def __str__(self):
        return self.user_id  # To give a string representation of the user
    
class SupportRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject