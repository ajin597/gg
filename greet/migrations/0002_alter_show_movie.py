# Generated by Django 5.0.2 on 2024-05-08 03:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='greet.movie'),
        ),
    ]
