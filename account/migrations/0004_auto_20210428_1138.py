# Generated by Django 3.2 on 2021-04-28 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_referral_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ps_authkey',
            field=models.CharField(blank=True, default=None, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ps_username',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]