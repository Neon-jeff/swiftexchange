# Generated by Django 4.2.6 on 2024-03-29 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_profile_trading_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='lost_trade',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]