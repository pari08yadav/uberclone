from django.db import models
from users.models import Users

# Create your models here.

class Ride(models.Model):
    STATUS_CHOICE = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    rider = models.ForeignKey(Users,on_delete=models.CASCADE, related_name="rides_as_rider")
    driver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="rides_as_driver", null=True, blank=True, default="")
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    pickup_latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True)
    pickup_longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True)
    drop_latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True)
    drop_longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='REQUESTED')
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rider_rating = models.FloatField(null=True, blank=True)
    driver_rating = models.FloatField(null=True, blank=True)
    rider_feedback = models.TextField(null=True, blank=True)
    driver_feedback = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Ride {self.id} - {self.status}"
