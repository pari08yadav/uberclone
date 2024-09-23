from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime, timedelta


# User model.
class Users(AbstractUser):
    
    USER_TYPE_CHOICES = (
        ('driver', 'Driver'),
        ('rider', 'Rider')
    )
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="")
    profile_picture_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.username

    class Meta:
        # Add this meta class to avoid clashes with the default user model
        swappable = 'AUTH_USER_MODEL'
        
        
# model for rest password
class PasswordResetToken(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=5)
    

# Driver profile model.
class DriverProfile(models.Model):
    VEHICLE_CHOICE = (
        ('car', 'Car'),
        ('auto', 'Auto'),
        ('bike', 'Bike')
    )
    
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_CHOICE, default="car")
    vehicle_registration_number = models.CharField(max_length=20, default="")
    years_of_experience = models.IntegerField(null=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.license_number}"
    
    