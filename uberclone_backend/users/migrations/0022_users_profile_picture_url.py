# Generated by Django 5.0.7 on 2024-08-04 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_driverprofile_license_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='profile_picture_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
