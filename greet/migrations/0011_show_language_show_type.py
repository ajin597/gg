# Generated by Django 5.0.2 on 2024-05-11 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greet', '0010_movie_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='language',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='type',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]