# Generated by Django 5.0.2 on 2024-05-08 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_razorpaypayment_payment_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='razorpaypayment',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='razorpaypayment',
            name='signature_id',
        ),
        migrations.RemoveField(
            model_name='razorpaypayment',
            name='status',
        ),
    ]
