# Generated by Django 5.0.2 on 2024-05-08 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_razorpaypayment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='razorpaypayment',
            name='status',
        ),
    ]
