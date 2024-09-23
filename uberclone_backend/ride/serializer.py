from rest_framework import serializers
from .models import Ride
from users.models import DriverProfile
from users.serializer import UserSerializer


class RideSerializer(serializers.ModelSerializer):
    driver = UserSerializer()
    rider = UserSerializer()
    
    class Meta:
        model = Ride
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['status'] = 'REQUESTED'
        return super().create(validated_data)
    


class RideRequestSerializer(serializers.ModelSerializer):
    # driver = UserSerializer()
    # rider = UserSerializer()
    
    class Meta:
        model = Ride
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['status'] = 'REQUESTED'
        return super().create(validated_data)
    
    
    

class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = ['latitude', 'longitude']
        


    