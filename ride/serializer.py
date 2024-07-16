from rest_framework import serializers
from .models import Ride


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['status'] = 'REQUESTED'
        return super().create(validated_data)
    