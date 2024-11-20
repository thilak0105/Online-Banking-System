from django.contrib import admin
from .models import *


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('trans_id', 'trans_time', 'from_acc', 'to_acc','trans_amt','trans_status')  # Replace with actual field names

admin.site.register(transactions, TransactionsAdmin)


admin.site.register(customer)
admin.site.register(employee)
admin.site.register(account)
admin.site.register(atm_cards)
admin.site.register(acc_atm_cards)
#admin.site.register(transactions)
admin.site.register(loan)
admin.site.register(installments)
admin.site.register(customer_credentials)
admin.site.register(employee_credentials)
admin.site.register(CustomUser)