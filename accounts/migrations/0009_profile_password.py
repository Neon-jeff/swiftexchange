# Generated by Django 4.2.6 on 2024-08-27 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_profile_address_document_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='password',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
