# Generated by Django 4.2.4 on 2023-09-03 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_remove_vendorprofile_about_and_more'),
        ('property', '0003_alter_property_vendor_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='vendor_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendorprofile'),
        ),
    ]
