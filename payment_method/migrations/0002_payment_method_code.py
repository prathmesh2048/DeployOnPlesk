# Generated by Django 3.2 on 2021-04-23 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_method', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_method',
            name='code',
            field=models.CharField(default=None, max_length=20, unique=True),
        ),
    ]
