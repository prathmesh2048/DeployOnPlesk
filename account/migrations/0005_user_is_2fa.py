# Generated by Django 3.2 on 2021-05-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210428_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_2fa',
            field=models.BooleanField(default=False),
        ),
    ]