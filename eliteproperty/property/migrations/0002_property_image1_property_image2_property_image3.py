# Generated by Django 4.2.4 on 2023-09-03 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
        migrations.AddField(
            model_name='property',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
        migrations.AddField(
            model_name='property',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]
