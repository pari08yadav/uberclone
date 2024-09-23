from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializer import SignupSerializer, LoginSerializer, UserDetailSerializer, UserSerializer, DriverProfileSerializer, DriverLocationSerializer,  UdateUserProfilePictureSerializer
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
            return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)
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
            'data': user_serializer.data,
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
@permission_classes([IsAuthenticated])
@csrf_exempt
def user_list(request):
    # if request.user.is_authenticated:
    if request.method == 'GET':
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"data": serializer.data})
    

# user update api
@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def user_profile_update(request):
    user = request.user
    try:
        data = request.data
    except:
        return Response({"error":"Data is not provided, please provide data."})
    
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=data)
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"data":serializer.data})
    return Response({"error":serializer.error}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def update_user_profile_picture(request):
    user = request.user
    profile_picture = request.FILES.get('profile_picture', None)
    print(profile_picture)
    if not profile_picture:
        return Response({'error':"No profile picture provided"}, status=400)
    
    # Upload image to Cloudinary (or any other third-party service)
    upload_result = upload(profile_picture)
    profile_picture_url = upload_result.get('url')
    
    user.profile_picture_url = profile_picture_url
    user.save()
    
    serializer = UserSerializer(user)
    return Response({"data":serializer.data}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def user_details(request):
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
@csrf_exempt 
def password_reset_request(request):
    # if request.user.is_authenticated:
    if request.method == "POST":
        data = request.data
        # email = data['email']
        email = request.user.email
        print(email)
        try:
            user = Users.objects.get(email=email)
            print(user)
        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # generate token using secret module.
        token = secrets.token_urlsafe(25)
        
        try:
            PasswordResetToken.objects.create(user=user, token=token)
        except:
            return Response({"error": "Token not found"})
        
        subject = 'If you did not request a new password, please ignore this message.'
        body = f'Please click the following link to reset your password: http://127.0.0.1:5173/reset_password/{token}/'
        sender_email = 'yadav.parishram@gmail.com'  # email id of sender mail
        recipient_email = email
        
        send_mail(subject, body, sender_email, [recipient_email], fail_silently=False,)
        
        return Response({"message":"Your reset password email is heading your way."}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# password reset confirm api
@api_view(['POST'])
@csrf_exempt 
def password_reset_confirm(request, token):
    print(token)
    if request.method == "POST":
        try:
            data = request.data
            new_password = data['new_password']
            print(new_password)
        except:
            return Response({"error":"Please enter new password..."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token_object = PasswordResetToken.objects.get(token=token)
        except: 
            return Response({"error":"token object not found, Please try again. "}, status=status.HTTP_400_BAD_REQUEST)
        
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
        print()
        return Response({"message":"Your password has been changed."})
        
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        

# Driver Location Update
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def update_driver_location(request):
#     user = request.user
#     data = request.data
    
#     try:
#         driver_profile = DriverProfile.objects.get(user=user)
#         driver_profile.latitude = data['latitude']
#         driver_profile.longitude = data['longitude']
#         driver_profile.save()
        
#         return Response({"message": "Location updated successfully."})
#     except DriverProfile.DoesNotExist:
#         return Response({'error': "Driver profile not found."}, status=status.HTTP_404_NOT_FOUND)


# Update Driver Location API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def update_driver_location(request):
    if request.method == "POST":
        # print("POST request received")  # Add logging to confirm POST request
        try:
            driver_profile = request.user.driver_profile
            print(f"Driver profile: {driver_profile}")
        except DriverProfile.DoesNotExist:
            return Response({"error":"Driver profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        # print(f"Request data: {data}")  # Log the received data
        
        if 'latitude' in data and 'longitude' in data:
            try:
                data['latitude'] = round(float(data['latitude']), 6)
                data['longitude'] = round(float(data['longitude']), 6)
            except (ValueError, TypeError):
                return Response({'error': 'Invalid latitude or longitude values.'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'error': 'Latitude and longitude are required.'}, status=status.HTTP_400_BAD_REQUEST)

        
        serializer = DriverLocationSerializer(data=data)
        # print(f"Serializer: {serializer}")
        
        if serializer.is_valid():
            driver_profile.latitude = serializer.validated_data['latitude']
            driver_profile.longitude = serializer.validated_data['longitude']
            driver_profile.save()
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            # print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error":"method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# create driver profile api
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def create_driver_profile(request):
    # if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.user_type == 'driver':
                data = request.data.copy()
                data['user'] = request.user.id
                print(request.user.id)
                # print(data)
                serializer = DriverProfileSerializer(data=data)
                # print(serializer)
                if serializer.is_valid(): 
                    driver_profile = serializer.save()
                    profile_picture = request.POST.get('profile_picture', None)
                    print(driver_profile)
                    if profile_picture:
                        upload_result = upload(profile_picture)
                        driver_profile.profile_picture_url = upload_result.get('url')
                        driver_profile.save()

                    response_serializer = DriverProfileSerializer(profile_picture)
                    return Response({"data":response_serializer.data})
                
                return Response({"error from serializer is_valid":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
            return Response({"error":"Create Driver type user profile."})
        
        return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # return Response({"error":"user is not authenticated"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def check_driver_profile(request):
    try:
        print(request.user)
        driver_profile = DriverProfile.objects.get(user=request.user)
        print(driver_profile)
        serializer = DriverProfileSerializer(driver_profile)
        return Response({"driver_profile":serializer.data})
    except DriverProfile.DoesNotExist:
        print("Driver profile is not found")
        return Response({'error':'Driver profile doest not exist.'}, status=status.HTTP_404_NOT_FOUND)

    


# Get Driver Profile API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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


