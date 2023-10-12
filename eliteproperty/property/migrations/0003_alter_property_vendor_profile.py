# Generated by Django 4.2.4 on 2023-09-03 05:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0002_property_image1_property_image2_property_image3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='vendor_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
