# Generated by Django 5.0.7 on 2024-07-17 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_users_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverprofile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
