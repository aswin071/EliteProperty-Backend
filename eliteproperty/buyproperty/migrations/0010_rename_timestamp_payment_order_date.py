# Generated by Django 4.2.4 on 2023-09-11 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyproperty', '0009_payment_order_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='timestamp',
            new_name='order_date',
        ),
    ]