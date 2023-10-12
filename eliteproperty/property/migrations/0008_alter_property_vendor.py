# Generated by Django 4.2.4 on 2023-09-04 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0007_rename_vendor_profile_property_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
