# Generated by Django 3.2 on 2021-08-07 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_method', '0004_paymentcreds_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentcreds',
            name='key',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
