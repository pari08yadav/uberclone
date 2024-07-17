from rest_framework import serializers
from .models import Users, DriverProfile
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'phone_number', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}


# User Signup Serilizer.
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only =True)
    
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'password', 'phone_number', 'user_type']
        
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
    
    class Meta:
        model = DriverProfile
        fields = '__all__'
        read_only_fields = ('id', 'profile_picture_url')  # ID and profile_picture_url are read-only
