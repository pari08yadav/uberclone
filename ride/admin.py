from django.contrib import admin
from .models import Ride

# Register your models here.

@admin.register(Ride)
class RideModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'rider', 'driver', 'pickup_location', 'drop_location', 'status', 'fare', 'created_at', 'updated_at']
    

    