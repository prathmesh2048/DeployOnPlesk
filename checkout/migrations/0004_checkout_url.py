# Generated by Django 3.2 on 2021-08-26 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20210811_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]