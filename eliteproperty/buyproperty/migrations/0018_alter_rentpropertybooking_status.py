# Generated by Django 4.2.4 on 2023-09-24 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyproperty', '0017_alter_propertybooking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentpropertybooking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('complete', 'Complete'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]