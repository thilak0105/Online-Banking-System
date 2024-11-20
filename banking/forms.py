from django import forms
from banking.models import *
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError

from django import forms
from .models import SupportRequest

class SupportRequestForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
class PasswordResetForm(forms.Form):
    cin = forms.IntegerField(required=True)
    user_id = forms.CharField(max_length=100, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

def check_acc_exits(value):
    if len(str(value)) != 10:
        raise ValidationError("Account number invalid.")
    
    if not account.objects.filter(acc_no=value).exists():
        raise ValidationError("Account does not exist.")

class trans_form(forms.Form):
    def __init__(self, *args, **kwargs):
        cin = kwargs.pop('cin', None) 
        super().__init__(*args, **kwargs)
        
        if cin:
            self.fields['from_acc'].queryset = account.objects.filter(cin=cin) # type: ignore

    from_acc = forms.ModelChoiceField(
        queryset=account.objects.none(),
        label="From Account",
        empty_label="Select Account"
    )
    
    to_acc = forms.IntegerField(
        label='To Account',
        validators=[MaxValueValidator(10000000000), MinValueValidator(1000000000),check_acc_exits]
    )
    
    trans_amt = forms.DecimalField(
        label='Amount',
       # widget=forms.Textarea(attrs={'placeholder': 'Enter amount to transfer'}),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(10000000)]
    )

    remarks = forms.CharField(
        label="Remarks",
        widget=forms.Textarea(attrs={'placeholder': 'No remarks'}),
        max_length=1000,
        required=False,
        initial='No remarks',
    )

def check_installemt_exits(value):
    if len(str(value)) != 12:
        raise ValidationError("Loan Account number invalid!")
    
    if not loan.objects.filter(loan_id=value).exists():
        raise ValidationError("Loan Account does not exist!")


from django import forms
from .models import account, loan  # Adjust this import as necessary

class InstallmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        cin = kwargs.pop('cin', None)  # Extract 'cin' from kwargs
        loan_obj = kwargs.pop('loan_obj', None)  # Extract 'loan_obj' from kwargs
        super().__init__(*args, **kwargs)  # Call the parent class's constructor

        # Set the queryset for 'from_acc' and 'to_loan_no' based on 'cin'
        if cin:
            self.fields['from_acc'].queryset = account.objects.filter(cin=cin)
            self.fields['to_loan_no'].queryset = loan.objects.filter(customer_id=cin)

        # Initialize due_amt with loan_obj's due_amt value if available
        if loan_obj:
            self.fields['due_amt'].initial = loan_obj.due_amt

    from_acc = forms.ModelChoiceField(
        queryset=account.objects.none(),
        label="From Account",
        empty_label="Select Account"
    )
    
    to_loan_no = forms.ModelChoiceField(
        queryset=loan.objects.none(),
        label="Loan Account",
        empty_label="Select Loan Account"
    )

    # Display due_amt field (readonly)
    due_amt = forms.DecimalField(
        label='Due Amount',
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )





class EmpPasswordResetForm(forms.Form):
    user_id = forms.CharField(max_length=100, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        

class AccountFreezeForm(forms.Form):
    account_choices = forms.ModelChoiceField(
        queryset=None,  # Will be set dynamically in the view
        label="Select Account",
        empty_label="Select an account to freeze",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        cin = kwargs.pop('cin', None)
        super(AccountFreezeForm, self).__init__(*args, **kwargs)
        if cin:
            self.fields['account_choices'].queryset = account.objects.filter(cin=cin)


class CashDepositForm(forms.Form):
    acc_no = forms.IntegerField(label='Account Number')
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)

    def clean_acc_no(self):
        acc_no = self.cleaned_data.get('acc_no')
        if not account.objects.filter(acc_no=acc_no).exists():
            raise ValidationError("Account does not exist!")
        return acc_no
    

class LoanInstallmentForm(forms.Form):
    loan_id = forms.IntegerField(label='Loan ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    trans_amt = forms.DecimalField(label='Transaction Amount', max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        loan = kwargs.pop('loan', None)
        super().__init__(*args, **kwargs)

        # If loan object is passed, set initial value for trans_amt (due_amt)
        if loan:
            self.fields['trans_amt'].initial = loan.due_amt

    # Validator to check if the loan exists
    def clean_loan_id(self):
        loan_id = self.cleaned_data.get('loan_id')
        if not loan.objects.filter(loan_id=loan_id).exists():
            raise ValidationError("Loan does not exist!")
        return loan_id

class AccountUnfreezeForm(forms.Form):
    acc_no = forms.CharField(label="Account Number", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_acc_no(self):
        acc_no = self.cleaned_data.get('acc_no')
        # Check if the account exists
        if not account.objects.filter(acc_no=acc_no).exists():
            raise ValidationError("Account does not exist!")
        return acc_no