from django.db import models
from ride.models import Ride
from datetime import datetime
from django.utils import timezone
# Create your models here.


class Payment(models.Model):
    STATUC_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'failed'),
    )
    
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUC_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)   
    
    def __str__(self):
        return f"Payment for Ride {self.ride.id} - {self.amount}"