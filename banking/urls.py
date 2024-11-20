from django.urls import path
from . import views
from .views import user_login

urlpatterns = [
    path('', views.members, name='members'),
    path('success/', views.success_page, name='success_page'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<int:cin>/', views.profile, name='profile'),
    path('reset-password/', views.password_reset_view, name='reset_password'),
    path('bill-pay/', views.bill_pay, name='bill_pay'),
    path('loans/', views.loans, name='loans'), 
    path('support/', views.support, name='support'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    path('home/', views.user_home, name='home'),
    path('trans/',views.transactionview,name='transferview'),
    path('manage_cards/',views.manage_cards,name='manage_cards'),
    path('edit_card_limit/<int:card_no>/', views.edit_card_limit, name='edit_card_limit'),
    path('pay-loan/',views.loan_pay_view,name='pay-loan'),
    path('emplogin/', views.employee_login, name='employee_login'),
    path('emphome/', views.employee_home, name='emphome'),
    path('emplogout/', views.employee_logout, name='employee_logout'),
    path('emp-reset-password/', views.employee_password_reset_view, name='emp_reset_password'),
    path('about/', views.about, name='about'),
    path('deposit/', views.make_installment, name='loan'),
    path('ajax/make_installment/', views.ajax_make_installment, name='ajax-make-installment'),
    path('ajax_installment/', views.ajax_make_installment, name='ajax_make_installment'),
    path('deposit_Cash/',views.cash_deposit, name='cashdeposit'),
    path('freeze_emp/',views.freeze_account, name='freeze'),

  # New AJAX URL

    path('freeze-acc/',views.freeze_account_view,name='freeze-acc'),
    path('unfreeze_acc/', views.unfreeze_account_view, name='unfreeze-account'),
    path('pay-loan/', views.loan_pay_view, name='loan_pay_view'),
    path('get-loan-due-amount/<int:loan_id>/', views.get_loan_due_amount, name='get_loan_due_amount'),
]