# Generated by Django 3.2 on 2021-04-23 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210421_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='referral_code',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
