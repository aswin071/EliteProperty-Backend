# Generated by Django 4.2.4 on 2023-09-04 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_alter_property_vendor_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='status',
        ),
    ]
