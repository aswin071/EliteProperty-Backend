# Generated by Django 4.2.4 on 2023-09-04 07:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_remove_property_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='address',
            field=models.CharField(default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='property',
            name='list_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
