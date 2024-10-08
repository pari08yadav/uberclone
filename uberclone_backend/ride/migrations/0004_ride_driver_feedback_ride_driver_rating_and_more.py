# Generated by Django 5.0.7 on 2024-07-17 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0003_alter_ride_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='driver_feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='driver_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='rider_feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='rider_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
