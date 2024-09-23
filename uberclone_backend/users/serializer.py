from rest_framework import serializers
from .models import Users, DriverProfile
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'phone_number', 'user_type', 'profile_picture_url']
        extra_kwargs = {'password': {'write_only': True},
                        # 'phone_number': {'write_only': True},
                        }
        
        
class UdateUserProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['profile_picture_url']


# User Signup Serilizer.
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only =True)
    
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'password', 'phone_number', 'user_type']
        extra_kwargs = {
            'phone_number': {'write_only': True}
        }
        
    def validate(self, data):
        return data
        
    def create(self, validated_data):
        user = Users(
            username = validated_data['username'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
            user_type = validated_data['user_type']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        return user
        
    
    
# User Login Serilizer.
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
            model = Users
            fields = ['username', 'password']
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
            
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is deactivated.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid login credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        
        return data
    
    
# serializer for user detail when user login
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'phone_number', 'user_type']

    def to_representation(self, instance):
        res =  super().to_representation(instance)
        return res
    

# serializer for driver profile
class DriverProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = DriverProfile
        fields = ['user', 'license_number', 'vehicle_type', 'vehicle_registration_number', 'years_of_experience', 'profile_picture_url', 'latitude', 'longitude', 'last_updated']
        read_only_fields = ('id', 'profile_picture_url','last_updated' )  # ID and profile_picture_url are read-only
        
        
# serializer for driver profile
class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = ['latitude', 'longitude']
        