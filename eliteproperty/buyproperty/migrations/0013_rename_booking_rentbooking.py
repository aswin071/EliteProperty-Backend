# Generated by Django 4.2.4 on 2023-09-11 18:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_alter_property_vendor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('buyproperty', '0012_order_propertybooking_delete_payment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Booking',
            new_name='RentBooking',
        ),
    ]
