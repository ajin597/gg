# Generated by Django 5.0.2 on 2024-05-08 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greet', '0005_delete_bookingpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
