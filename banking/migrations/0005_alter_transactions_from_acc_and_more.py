# Generated by Django 5.1.1 on 2024-10-22 19:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0004_alter_customuser_options_alter_account_acc_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='from_acc',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='transactions_from_account', to='banking.account', verbose_name='From Account'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='to_acc',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='transactions_to_account', to='banking.account', verbose_name='To Account'),
        ),
    ]