# Generated by Django 5.1.1 on 2024-10-22 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0002_loan_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installments',
            name='installment_id',
            field=models.BigIntegerField(blank=True, primary_key=True, serialize=False, unique=True, verbose_name='Transaction ID'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_id',
            field=models.BigIntegerField(blank=True, primary_key=True, serialize=False, unique=True),
        ),
    ]
