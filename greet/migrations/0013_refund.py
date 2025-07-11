# Generated by Django 5.1.5 on 2025-03-29 06:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greet', '0012_booking_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100, unique=True)),
                ('refund_id', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processed', 'Processed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
