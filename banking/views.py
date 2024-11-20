from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.http import HttpResponse
from django.template import loader
from django.db import transaction
from .models import CustomUser, customer, account, installments, loan, transactions, customer_credentials
from .backends import CustomAuthBackend 
from banking.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from banking.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from .models import *
from datetime import date
from itertools import chain


def profile(request, cin):
    print("Profile view accessed with CIN:", cin)
    
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, 'You need to log in to access your profile.')
        return redirect('login')
    
    try:
        # Ensure CIN is a valid integer
        cin = int(cin)

        # Get the customer using the provided CIN
        customer_details = customer.objects.get(cin=cin)

        # Check if the logged-in user has permission to view this profile
        if customer_details.cin != request.session.get('cin_id'):
            messages.error(request, 'You do not have permission to view this profile.')
            return redirect('home')

        # Fetch all account information associated with this customer
        account_details = account.objects.filter(cin=customer_details.cin)

        # Prepare the context with data from both tables
        context = {
            'customer': customer_details,
            'accounts': account_details,  # Pass a list of accounts to the template
            'phone': customer_details.phone,
            'email': customer_details.email,
        }

        return render(request, 'profile.html', context)

    except ValueError:
        messages.error(request, 'Invalid CIN provided. Please check your input.')
        return redirect('home')
    
    except customer.DoesNotExist:
        messages.error(request, 'Customer not found. Please contact support.')
        return redirect('home')
    
    except Exception as e:
        messages.error(request, 'An error occurred: {}'.format(str(e)))
        return redirect('home')

def user_home(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            # Fetch customer info using the stored session user_id
            customer_info = customer_credentials.objects.get(user_id=user_id)
            name = customer.objects.get(cin=customer_info.cin_id)
            #print(name)
            # Debugging: Print session data
            print(f"User ID from session: {user_id}, CIN: {customer_info.cin_id}")

            # Fetch all accounts related to the CIN from customer_info
            accounts = account.objects.filter(cin=customer_info.cin_id)

            # Initialize acc_balance to None
            acc_balance = None
            
            # If there are accounts, get the balance of the first account
            if accounts.exists():
                acc_balance = accounts.first().acc_balance  # Get the balance from the first account
            
            # Fetch the last 5 successful transactions for the logged-in user
            recent_transactions = transactions.objects.filter(
                trans_status='S',  # Filter for successful transactions
                from_acc__cin=customer_info.cin_id  # Filter by CIN of the account
            ).order_by('-trans_time')[:5]  # Order by transaction time in descending order and limit to 5
            


            # Pass the customer object, accounts, account balance, and recent transactions to the template
            return render(request, 'home.html', {
                'customer': customer_info,
                'accounts': accounts,
                'acc_balance': acc_balance,
                'recent_transactions': recent_transactions,
                'name' : name,
            })

        except customer_credentials.DoesNotExist:
            messages.error(request, 'User not found. Please log in again.')
            return redirect('login')
    else:
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')
    
def user_login(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input').strip()  # Get user input
        password = request.POST.get('password').strip()  # Get password

        user = authenticate(request, user_id=user_input, password=password)

        if user is not None:
            login(request, user)  # Log in the user
            
            # Retrieve the related customer_credentials to access CIN
            try:
                customer_info = customer_credentials.objects.get(user_id=user.user_id)
                request.session['cin_id'] = customer_info.cin_id  # Store CIN in session
            except customer_credentials.DoesNotExist:
                messages.error(request, 'CIN not found for this user. Please contact support.')
                return redirect('login')

            request.session['user_id'] = user.user_id  # Store user_id in session
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, 'Invalid user ID or password. Please try again.')

    return render(request, 'login.html')

def employee_login(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input').strip()  # Get the employee user_id
        password = request.POST.get('password').strip()      # Get the employee password

        # Authenticate the user using your custom backend
        user = authenticate(request, user_id=user_input, password=password)

        if user is not None:
            login(request, user)  # Log in the user
            try:
                employee_info = employee_credentials.objects.get(user_id=user.user_id)
                request.session['employee_id'] = employee_info.employee_id_id  # Store CIN in session
            except customer_credentials.DoesNotExist:
                messages.error(request, 'Employee_id not found for this user. Please contact support.')
                return redirect('members')
            request.session['user_id'] = user.user_id  # Store user_id in the session
            return redirect('emphome')  # Redirect to the employee home page
        else:
            messages.error(request, 'Invalid user ID or password. Please try again.')

    return render(request, 'emplogin.html')

def employee_home(request):
    user_id = request.session.get('user_id')
    emp = employee_credentials.objects.get(user_id=user_id)

    # Get all customers managed by the employee
    cust = customer.objects.filter(managed_by=emp.employee_id)

    # Get all account records where the customer's CIN is in the list of customer CINs
    accounts = account.objects.filter(cin__in=[i.cin for i in cust])

    # Fetch counts based on account status
    active_accounts_count = accounts.filter(acc_status='A').count()  # Count active accounts
    low_balance_accounts_count = accounts.filter(acc_status='L').count()  # Count low balance accounts

    context = {
        'accounts': accounts,
        'active_accounts_count': active_accounts_count,
        'low_balance_accounts_count': low_balance_accounts_count,
    }
    
    return render(request, 'emphome.html', context)

def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            cin = form.cleaned_data["cin"]
            user_id = form.cleaned_data["user_id"]
            new_password = form.cleaned_data["new_password"]

            try:
                # Fetch the customer credentials using the provided CIN and user_id
                credentials = customer_credentials.objects.get(cin=cin, user_id=user_id)
                
                hashed_password = make_password(new_password)
                # Directly set the new password without hashing
                credentials.password = new_password  
                credentials.save()
                
                try:
                    custom_user = CustomUser.objects.get(user_id=user_id)
                    custom_user.password = hashed_password  # Update the password in CustomUser
                    custom_user.save()

                    messages.success(request, "Password successfully changed")
                except CustomUser.DoesNotExist:
                    messages.error(request, "CustomUser not found. Please contact support.")


                return redirect('login')

            except customer_credentials.DoesNotExist:
                form.add_error(None, "CIN or User ID is incorrect.")
    
    else:
        form = PasswordResetForm()

    return render(request, 'reset_password.html', {'form': form})

def user_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def employee_logout(request):
    logout(request) 
    request.session.flush() # This will log the user out
    return redirect('members')

# View for the success page after login (optional)
def success_page(request):
    return render(request, 'success.html')

# Bill payment page view
def bill_pay(request):
        user_id = request.session.get('user_id')
    
        if user_id:
            try:
                customer_info = customer_credentials.objects.get(user_id=user_id)  # Fetch full customer credentials
                return render(request, 'bill-pay.html', {'customer': customer_info})  # Pass the entire customer object
            except customer_credentials.DoesNotExist:
                messages.error(request, 'Customer not found. Please log in again.')
                return redirect('login')
        else:
            messages.error(request, 'You must be logged in to view this page.')
            return redirect('login')

# Loans page view
def loans(request):
    user_id = request.session.get('user_id')  # Get the user ID from the session
    
    if user_id:
        try:
            # Fetch the customer's credentials
            user_credentials = customer_credentials.objects.get(user_id=user_id)

            # Fetch the customer's details using the CIN from user credentials
            customer_info = get_object_or_404(customer, cin=user_credentials.cin.cin)

            # Filter loans based on the customer object
            loans = loan.objects.filter(customer=customer_info)
            installments_list = installments.objects.filter(loan_id__in=loans)
            context = {
                'loans': loans,
                'customer_info': customer_info,
            }
            return render(request, 'loans.html', context)
        
        except customer_credentials.DoesNotExist:
            messages.error(request, 'Customer not found. Please log in again.')
            return redirect('login')

    else:
        # If the user_id is not found in the session
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')

# Support page view
def support(request):
    # Fetch the user_id from the session
    user_id = request.session.get('user_id')

    if user_id:
        try:
            # Fetch customer credentials
            customer_info = customer_credentials.objects.get(user_id=user_id)  # Fetch full customer credentials
        except customer_credentials.DoesNotExist:
            messages.error(request, 'Customer not found. Please log in again.')
            return redirect('login')
    else:
        # If the user_id is not found in the session
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')

    # Handle form submission
    if request.method == 'POST':
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your support request has been submitted successfully.')
            return redirect('support')  # Redirect to clear the form after submission
    else:
        form = SupportRequestForm()

    # Render the page with customer info and form
    return render(request, 'support.html', {'form': form, 'customer': customer_info})

# Transaction history page view
@login_required
def transaction_history(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            # Fetch the customer's account based on the user_id
            customer_info = customer_credentials.objects.get(user_id=user_id)
            # Fetch all accounts related to the customer
            accounts = account.objects.filter(cin=customer_info.cin_id)
            transactions_list = transactions.objects.filter(from_acc__in=accounts) | transactions.objects.filter(to_acc__in=accounts)
            transactions_list = transactions_list.order_by('-trans_time')  # Order by transaction time descending
            
            # Pass accounts to the template
            return render(request, 'transaction-history.html', {
                'transactions': transactions_list,
                'customer': customer_info,
                'accounts': accounts  # Pass accounts to template
            })
        except customer_credentials.DoesNotExist:
            messages.error(request, 'User not found. Please log in again.')
            return redirect('login')
    else:
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')
    
# Members page view
def members(request):
    return render(request, 'index.html')

@login_required
def transactionview(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            # Fetch full customer credentials
            customer_info = customer_credentials.objects.get(user_id=user_id)
            cin = customer_info.cin_id  # Get the customer's CIN
            stored_mpin = customer_info.mpin  # Assuming MPIN is stored as an integer or string
            
            if request.method == 'POST':
                form = trans_form(request.POST, cin=cin)  # Pass the cin value during form initialization
                
                # Fetch and clean the entered MPIN
                entered_mpin = request.POST.get('mpin').strip()

                # Debugging: Print MPINs to check values
                print(f"Entered MPIN: {entered_mpin}, Stored MPIN: {stored_mpin}")

                # Convert the stored MPIN to string for comparison consistency
                if entered_mpin == str(stored_mpin):
                    if form.is_valid():
                        from_acc = form.cleaned_data['from_acc']
                        to_acc_no = form.cleaned_data['to_acc']
                        trans_amt = form.cleaned_data['trans_amt']
                        remark = form.cleaned_data['remarks']

                        # Convert to_acc_no to the account object
                        to_acc = get_object_or_404(account, acc_no=to_acc_no)
                        if from_acc.acc_status != 'A':
                            if from_acc.acc_status == 'F':
                                reason = 'Transaction failed: Account is Frozen.'
                            elif from_acc.acc_status == 'L':
                                reason = 'Transaction failed: Account has Low Balance.'
                            else:
                                reason = 'Transaction failed: Invalid account status.'
                            transaction_instance = transactions(
                                from_acc=from_acc,
                                to_acc=to_acc,
                                trans_amt=trans_amt,
                                trans_status='F',
                                remarks=reason,
                            )
                            transaction_instance.save()
                            messages.error(request, reason)
                        else:
                        # Check for sufficient balance
                            if from_acc.acc_balance >= trans_amt:
                                with transaction.atomic():
                                    # Update account balances
                                    from_acc.acc_balance -= trans_amt
                                    to_acc.acc_balance += trans_amt

                                    from_acc.save()
                                    to_acc.save()

                                    # Create the transaction instance manually
                                    transaction_instance = transactions(
                                        from_acc=from_acc,
                                        to_acc=to_acc,
                                        trans_amt=trans_amt,
                                        trans_status='S',
                                        remarks=remark
                                    )
                                    transaction_instance.save()

                                # Success message
                                messages.success(request, 'Transaction successful!')
                            else:
                                # Insufficient balance, create failed transaction record
                                transaction_instance = transactions(
                                    from_acc=from_acc,
                                    to_acc=to_acc,
                                    trans_amt=trans_amt,
                                    trans_status='F',
                                    remarks=remark
                                )
                                transaction_instance.save()
                                messages.error(request, 'Transaction failed: Insufficient balance.')
                    else:
                        messages.error(request, 'Invalid transaction details.')
                else:
                    # If MPIN does not match
                    messages.error(request, 'Invalid MPIN. Please try again.')

            else:
                # GET request, render form with CIN
                form = trans_form(cin=cin)  # Pass the CIN value to form initialization

            context = {
                'form': form,
                'customer': customer_info  # Pass the entire customer object for context
            }
            return render(request, 'transferview.html', context)

        except customer_credentials.DoesNotExist:
            # Handle case where customer is not found
            messages.error(request, 'Customer not found. Please log in again.')
            return redirect('login')

    else:
        # Redirect to login if not logged in
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')

def manage_cards(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            # Fetch customer info using the stored session user_id
            customer_info = customer_credentials.objects.get(user_id=user_id)

            # Fetch all accounts related to the CIN from customer_info
            accounts = account.objects.filter(cin=customer_info.cin_id)

            # Fetch all ATM cards linked to the user's accounts
            atm_cards_info = atm_cards.objects.filter(acc_no__in=accounts)

            # Pass the ATM cards and customer info to the template
            return render(request, 'manage_cards.html', {
                'customer': customer_info,
                'atm_cards': atm_cards_info,
                'accounts': accounts
            })

        except customer_credentials.DoesNotExist:
            messages.error(request, 'User not found. Please log in again.')
            return redirect('login')
    else:
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login')

def edit_card_limit(request, card_no):
    if request.method == 'POST':
        new_limit = request.POST.get('monthly_limit')
        
        try:
            # Fetch the ATM card and update its limit
            card = atm_cards.objects.get(card_no=card_no)
            card.monthly_limit = new_limit
            card.save()
            
            messages.success(request, 'Monthly limit updated successfully.')
        except atm_cards.DoesNotExist:
            messages.error(request, 'Card not found.')
    
    return redirect('manage_cards')

@login_required
def loan_pay_view(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        customer_info = customer_credentials.objects.get(user_id=user_id)
        cin = customer_info.cin_id  # Get the customer's CIN

    if request.method == 'POST':
        # Get the loan object for prepopulating due_amt
        loan_id = request.POST.get('to_loan_no')
        loan_obj = get_object_or_404(loan, loan_id=loan_id)

        form = InstallmentForm(request.POST, cin=cin, loan_obj=loan_obj)  # Pass cin and loan_obj

        if form.is_valid():
            from_acc = form.cleaned_data['from_acc']
            trans_amt = loan_obj.due_amt  # Get due_amt from loan object

            if from_acc.acc_balance >= trans_amt:
                with transaction.atomic():
                    from_acc.acc_balance -= trans_amt
                    loan_obj.loan_amt -= trans_amt

                    # Update loan's next installment date and status
                    loan_obj.next_inst_date += relativedelta(months=1)
                    loan_obj.loan_status = 'A'

                    if loan_obj.loan_amt <= 0:
                        loan_obj.loan_status = 'C'

                    from_acc.save()
                    loan_obj.save()

                    # Create the installment record
                    loan_instance = installments(
                        loan_id=loan_obj,
                        installment_amt=trans_amt,
                    )
                    loan_instance.save()

                    # Create transaction record
                    transaction_instance = transactions(
                        from_acc=from_acc,
                        to_acc=from_acc,
                        trans_amt=trans_amt,
                        trans_status='S',
                        remarks='Loan Payment against loan no: ' + str(loan_obj.loan_id)
                    )
                    transaction_instance.save()

                messages.success(request, 'Transaction successful!')

            else:
                # Handle insufficient balance
                messages.error(request, 'Transaction failed: Insufficient balance.')

    else:
        form = InstallmentForm(cin=cin)  # Pass cin for GET request

    context = {
        'form': form,
        'cin': cin  # Pass cin to context
    }
    return render(request, 'loanview.html', context)


def about(request):
    return render(request, 'about.html')

def employee_password_reset_view(request):
    if request.method == "POST":
        form = EmpPasswordResetForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data["user_id"]
            new_password = form.cleaned_data["new_password"]

            try:
                # Fetch the customer credentials using the provided CIN and user_id
                credentials = employee_credentials.objects.get(user_id=user_id)
                
                hashed_password = make_password(new_password)
                # Directly set the new password without hashing
                credentials.password = new_password  
                credentials.save()
                
                try:
                    custom_user = CustomUser.objects.get(user_id=user_id)
                    custom_user.password = hashed_password  # Update the password in CustomUser
                    custom_user.save()

                    messages.success(request, "Password successfully changed")
                except CustomUser.DoesNotExist:
                    messages.error(request, "CustomUser not found. Please contact support.")


                return redirect('login')

            except employee_credentials.DoesNotExist:
                # form.add_error(None, "CIN or User ID is incorrect.")
                messages.error(request, "CEmployee does not exist!")
                raise ValidationError('Employee does not exist!')
                
    
    else:
        form = EmpPasswordResetForm()

    return render(request, 'emp_reset_password.html', {'form': form})

@login_required
def freeze_account_view(request):
    user_id = request.session.get('user_id')

    if user_id:
        customer_info = customer_credentials.objects.get(user_id=user_id)
        cin = customer_info.cin_id  # Get the customer's CIN

    if request.method == 'POST':
        form = AccountFreezeForm(request.POST, cin=cin)
        if form.is_valid():
            # Get the selected account
            selected_acc = form.cleaned_data['account_choices']
            
            if selected_acc.acc_status == 'F':
                messages.warning(request, 'The account is already frozen.')
            else:
                # Freeze the selected account
                selected_acc.acc_status = 'F'
                selected_acc.save()
                messages.success(request, 'The account has been successfully frozen.')

            return redirect('freeze-acc')  # Redirect to account details page or desired page
    else:
        form = AccountFreezeForm(cin=cin)  # Pass CIN to the form to filter accounts

    context = {
        'form': form
    }
    return render(request, 'freeze_account.html', context)



@login_required
def cash_deposit(request):
    if request.method == 'POST':
        form = CashDepositForm(request.POST)
        if form.is_valid():
            acc_no = form.cleaned_data['acc_no']
            amount = form.cleaned_data['amount']
            
            # Fetch the account and update the balance
            acc = get_object_or_404(account, acc_no=acc_no)
            acc.acc_balance += amount
            acc.save()

            # Redirect to a success page or display a message
            messages.success(request, 'Deposit successful!')
            return redirect('emphome')

    else:
        form = CashDepositForm()

    return render(request, 'deposit_Cash.html', {'form': form})



from django.http import JsonResponse

@login_required
def get_loan_due_amount(request, loan_id):
    loan_obj = get_object_or_404(loan, loan_id=loan_id)
    due_amt = loan_obj.due_amt
    return JsonResponse({'due_amt': due_amt})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta

@login_required
def make_installment(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        loan_obj = get_object_or_404(loan, loan_id=loan_id)
        form = LoanInstallmentForm(request.POST, loan=loan_obj)

        if form.is_valid():
            amount = loan_obj.due_amt  # Due amount is auto-filled
            
            if loan_obj.loan_amt >= amount:
                loan_obj.loan_amt -= amount
                loan_obj.loan_status = 'A'  # Set status to 'ACTIVE' after payment
                loan_obj.next_inst_date += relativedelta(months=1)  # Move next installment date forward

                if loan_obj.loan_amt <= 0:  # Loan is fully paid
                    loan_obj.loan_status = 'C'  # Set status to 'COMPLETED'

                loan_obj.save()

                messages.success(request, 'Installment successful!')
                return redirect('emphome')  # Redirect to a success page or home

    else:
        loan_id = request.GET.get('loan_id')
        loan_obj = get_object_or_404(loan, loan_id=loan_id)
        form = LoanInstallmentForm(loan=loan_obj)

    return render(request, 'deposit.html', {'form': form})


@require_POST
@login_required
def ajax_make_installment(request):
    loan_id = request.POST.get('loan_id')
    loan_obj = get_object_or_404(loan, loan_id=loan_id)
    
    # Create a form instance with the POST data
    form = LoanInstallmentForm(request.POST, loan=loan_obj)

    if form.is_valid():
        amount = loan_obj.due_amt  # Due amount is auto-filled

        if loan_obj.loan_amt >= amount:
            # Deduct installment amount from loan amount
            loan_obj.loan_amt -= amount
            loan_obj.loan_status = 'A'  # Set status to 'ACTIVE' after payment
            loan_obj.next_inst_date += relativedelta(months=1)  # Move next installment date forward

            # Check if loan is fully paid
            if loan_obj.loan_amt <= 0:
                loan_obj.loan_status = 'C'  # Set status to 'COMPLETED'

            loan_obj.save()

            # Create installment record
            installment = installments(loan_id=loan_obj)
            installment.installment_amt = amount  # Set the installment amount
            installment.save()

            return JsonResponse({'success': True, 'message': 'Installment successful!'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient loan amount.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid data.'})


@login_required
def unfreeze_account_view(request):
    if request.method == 'POST':
        form = AccountUnfreezeForm(request.POST)
        
        if form.is_valid():
            acc_no = form.cleaned_data['acc_no']
            
            # Retrieve the account and change its status
            acc_obj = get_object_or_404(account, acc_no=acc_no)
            
            if acc_obj.acc_status == 'A':
                messages.warning(request, 'The account is already active.')
            else:
                acc_obj.acc_status = 'A'  # Set account status to 'Active'
                acc_obj.save()
                messages.success(request, 'The account has been successfully unfrozen.')

            return redirect('emphome')  # Redirect to home or account summary page
    else:
        form = AccountUnfreezeForm()

    return render(request, 'unfreeze_account.html', {'form': form})

@login_required
def freeze_account(request):
    if request.method == 'POST':
        form = AccountUnfreezeForm(request.POST)
        
        if form.is_valid():
            acc_no = form.cleaned_data['acc_no']
            
            # Retrieve the account and change its status
            acc_obj = get_object_or_404(account, acc_no=acc_no)
            
            if acc_obj.acc_status == 'F':
                messages.warning(request, 'The account is already frozen.')
            else:
                acc_obj.acc_status = 'F'  # Set account status to 'Freeze'
                acc_obj.save()
                messages.success(request, 'The account has been successfully frozen.')

            return redirect('emphome')  # Redirect to home or account summary page
    else:
        form = AccountUnfreezeForm()

    return render(request, 'freeze_emp.html', {'form': form})