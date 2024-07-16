from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.decorators import api_view
from .serializer import SignupSerializer, LoginSerializer, UserDetailSerializer, UserSerializer, DriverProfileSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .jwt_token import generate_jwt_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Users, PasswordResetToken, DriverProfile
import secrets
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from cloudinary.uploader import upload
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes




# Create your views here.

def home(request):
    return HttpResponse("<h1> Hello world </h1>")

# Signup api
@api_view(['POST'])
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            serializer.save()
            
            subject = 'Your signup is done'
            body = message = 'Welcome to uber, complete your ride with our best drivers.'
            sender_email = 'yadav.parishram@gmail.com'  # email id of sender mail
            recipient_email = user_email
            
            send_mail(subject, body, sender_email, [recipient_email], fail_silently=False,)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login api
@api_view(['POST'])
@csrf_exempt
def login(request):
    serializers = LoginSerializer(data=request.data)
    if serializers.is_valid():
        user = serializers.validated_data['user']
        token = generate_jwt_token(user)
        user_serializer = UserDetailSerializer(user)
        return Response({
            'user': user_serializer.data,
            'token': token 
            }, status=status.HTTP_200_OK)
    
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# Logout api
@api_view(['POST'])
@csrf_exempt
@login_required
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully.'})


# user_list api
@api_view(['GET'])
@csrf_exempt
def user_list(request):
    # if request.user.is_authenticated:
    if request.method == 'GET':
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"data": serializer.data})
    

@api_view(['GET'])
@csrf_exempt
def user_details(request, id):
    # if request.user.is_authenticated:
    try:
        user = request.user
        user = Users.objects.get(id=user.id)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_200_OK)
    
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response({"data":serializer.data})
    

# delete user api
@api_view(['DELETE'])
@csrf_exempt      
def user_delete(request):
    # if request.user.is_authenticated:
    try:
        user = request.user
        user = Users.objects.get(id=user.id)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_200_OK)
    
    if request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['POST'])
@csrf_exempt 
def password_reset_request(request):
    # if request.user.is_authenticated:
    if request.method == "POST":
        data = request.data
        email = data['email']
        
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # generate token using secret module.
        token = secrets.token_urlsafe(25)
        
        try:
            PasswordResetToken.objects.create(user=user, token=token)
        except:
            return Response({"error": "Token not found"})
        
        subject = 'If you did not request a new password, please ignore this message.'
        body = f'Please click the following link to reset your password: http://127.0.0.1:8000/reset_password/{token}/'
        sender_email = 'yadav.parishram@gmail.com'  # email id of sender mail
        recipient_email = email
        
        send_mail(subject, body, sender_email, [recipient_email], fail_silently=False,)
        
        return Response({"message":"Your reset password email is heading your way."}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# password reset confirm api
@api_view(['POST'])
@csrf_exempt 
def password_reset_confirm(request, token):
    if request.method == "POST":
        try:
            new_password = request.data.get('new_password')
        except:
            return Response({"error":"Please enter new password..."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token_object = PasswordResetToken.objects.get(token=token)
            
        except: 
            return Response({"error":"User not found, Please try again. "}, status=status.HTTP_400_BAD_REQUEST)
        
        if token_object.is_expired():
            return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST) 
        
        hash_new_password = make_password(new_password)
        user = token_object.user
        
        try:
            user_data = Users.objects.get(id=user.id)
        except Users.DoesNotExist:
            return Response({"message": "user is not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user_data.password = hash_new_password
        user_data.save()
        
        return Response({"message":"Your password has been changed."})
        
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        


# create driver profile api
@api_view(['POST'])
@csrf_exempt
@parser_classes([MultiPartParser, FormParser])
def create_driver_profile(request):
    # if request.user.is_authenticated:
    if request.method == "POST":
        data = request.data.copy()
        data['user'] = request.user.id
        print(data)
        serializer = DriverProfileSerializer(data=data)
        if serializer.is_valid(): 
            driver_profile = serializer.save()
            profile_picture = request.POST.get('profile_picture', None)
            
            if profile_picture:
                upload_result = upload(profile_picture)
                driver_profile.profile_picture_url = upload_result.get('url')
                driver_profile.save()

            response_serializer = DriverProfileSerializer(profile_picture)
            return Response({"data":response_serializer.data})
        
        return Response({"error from serializer is_valid":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# Get Driver Profile API
@api_view(['GET'])
@csrf_exempt
def get_driver_profile(request):
    # if request.user.is_authenticated:
    if request.method == "GET":
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
        except DriverProfile.DoesNotExist:
            return Response({"error": "Driver profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DriverProfileSerializer(driver_profile)
        return Response(serializer.data)

    return Response({"error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# Update Driver Profile Api
@api_view(['PUT'])
@csrf_exempt
@parser_classes([MultiPartParser, FormParser])
def update_driver_profile(request):
    # if request.user.is_authenticated:
    try:
        driver_profile = DriverProfile.objects.get(user=request.user)
    except DriverProfile.DoesNotExist:
        return Response({"error": "Driver profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        data = request.data.copy()
        data['user'] = request.user.id
    except:
        return Response({"message": "Data is not given."})
    
    serializer = DriverProfileSerializer(driver_profile, data=data)
    if serializer.is_valid():
        driver_profile = serializer.save()
        
        profile_picture = request.POST.get('profile_picture', None)
        if profile_picture:
            upload_result = upload(profile_picture)
            driver_profile.profile_picture_url = upload_result.get('url')
            driver_profile.save()
            
        return Response({"data",serializer.data}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# driver profile partially update api...
@api_view(['PATCH'])
@csrf_exempt
@parser_classes([MultiPartParser, FormParser])
def update_driver_profile_partially(request):
    # if request.user.is_authenticated:
    try:
        driver_profile = DriverProfile.objects.get(user=request.user)
    except DriverProfile.DoesNotExist:
        return Response({"error": "Driver profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data['user'] = request.user.id
    
    serializer = DriverProfileSerializer(driver_profile, data=data, partial=True)
    if serializer.is_valid():
        driver_profile = serializer.save()
        
        profile_picture = request.POST.get('profile_picture', None)
        if profile_picture:
            upload_result = upload(profile_picture)
            driver_profile.profile_picture_url = upload_result.get('url')
            driver_profile.save()
            
        return Response({"message":serializer.data}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


