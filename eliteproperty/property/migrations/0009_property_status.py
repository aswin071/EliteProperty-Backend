# Generated by Django 4.2.4 on 2023-09-13 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_alter_property_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Reserved', 'Reserved'), ('Sold', 'Sold')], default='Available', max_length=20),
        ),
    ]
