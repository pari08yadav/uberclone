from django.shortcuts import render
import random, json
import requests
import os
from distance_calculate import haversine_distance
from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .serializer import RideSerializer, DriverLocationSerializer, RideRequestSerializer
from .models import Ride
from rest_framework.permissions import IsAuthenticated
from users.models import DriverProfile
from django.views.decorators.csrf import csrf_exempt
from email_send import send_ride_email_request, send_ride_rejected_email, send_ride_accepted_email



# Create Ride API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_ride(request):
    # if request.user.is_authenticated:
    if request.method == 'POST':
        data = request.data
        data['rider'] = request.user.id
        serializer = RideSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"serializer.data"}, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# # Get Ride API.
# @api_view(['GET'])
# @csrf_exempt
# def get_ride(request, ride_id):
#     try:
#         ride = Ride.objects.get(id=ride_id)
#     except Ride.DoesNotExist:
#         return Response({"error":"ride not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     serializer = RideSerializer(ride)
#     return Response({"data":serializer.data})


# Update Ride API.
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def udpate_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    if request.method == "PUT":
        serializer = RideSerializer(ride, data=data)
    else:
        serializer = RideSerializer(ride, data=data, partial=True)
        
    if serializer.is_valid():
        serializer.save()
        return Response({"data":serializer.data})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# list all Ride
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def list_rides(request):
    # if request.user.is_authenticated:
    if hasattr(request.user, 'driver_profile'):
        rides = Ride.objects.filter(driver=request.user)
    else:
        rides = Ride.objects.filter(rider=request.user)
    serializer = RideSerializer(rides, many=True)
    return Response({"data":serializer.data})



# Delete ride api 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def delete_ride(request, ride_id):
    # if request.user.is_authenticated:
    if request.method == "DELETE":
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)
        
        ride.delete()
        return Response({"message":"Ride Deleted Successfully."}, status=status.HTTP_204_NO_CONTENT)

    return Response({"error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# GeoCode API
@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def geocode_address(request):
    address = request.query_params.get('address')
    if not address:
        return Response({'error': 'Address parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # access_token = os.getenv('MAP_MY_INDIA_ACCESS_TOKEN')
    # url = f'https://atlas.mappls.com/api/places/geocode'
    
    headers = {
        'User-Agent': 'YourAppName/1.0 (your.email@example.com)'  # Include your app name and email
    }
    url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1'

    
    # if not access_token:
    #     return Response({'error': 'API token is missing'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        data = response.json()
        
        if not data:
            return Response({'error': 'No results found for the provided address'}, status=status.HTTP_404_NOT_FOUND)

        result = data[0]
        latitude = result.get('lat')
        longitude = result.get('lon')
        
        if not latitude or not longitude:
            return Response({'error': 'Latitude and longitude not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'latitude': latitude,
            'longitude': longitude
        })
    
        
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return Response({'error': 'HTTP Error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return Response({'error': 'Error Connecting to the server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return Response({'error': 'Request timed out'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def autocomplete_address(request):
    query = request.GET.get('query')
    if not query:
        return JsonResponse({'error': 'Query parameter is required'}, status=400)
    
    access_token = os.getenv('MAP_MY_INDIA_ACCESS_TOKEN')
    print(access_token)
    url = 'https://atlas.mapmyindia.com/api/places/search/json'
    try:
        response = requests.get(
            url,
            params={'query': query, 'location': '28.6139,77.2090', 'region': 'ind'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        # print(response.json())
        response.raise_for_status()  # Raises a HTTPError if the response code was unsuccessful
        data = response.json()
        
        # print("MapMyIndia Response: ", data)
        
        suggested_locations = data.get('suggestedLocations', [])
        if not suggested_locations:
            return JsonResponse({'error': 'No suggestions found'}, status=404)

        # # Respond with the list of suggestions
        # return JsonResponse({'suggestedLocations': suggested_locations}, status=200)
        
        
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        return JsonResponse({'error': 'HTTP Error occurred'}, status=500)
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return JsonResponse({'error': 'Error Connecting to the server'}, status=500)
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return JsonResponse({'error': 'Request timed out'}, status=500)
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
        return JsonResponse({'error': 'An error occurred'}, status=500)
    
    return JsonResponse(response.json())

    
# Request Ride API
@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def request_ride(request):
    # if request.user.is_authenticated:
        if request.method == "POST":
            data = request.data
            data['rider'] = request.user.id
            
            
            # Round latitude and longitude to 10 decimal places
            try:
                pickup_latitude = round(float(data['pickup_latitude']), 10)
                pickup_longitude = round(float(data['pickup_longitude']), 10)
                drop_latitude = round(float(data['drop_latitude']), 10)
                drop_longitude = round(float(data['drop_longitude']), 10)
            except (ValueError, KeyError):
                return Response({'error': 'Invalid latitude or longitude'}, status=status.HTTP_400_BAD_REQUEST)
        
            
            serializer = RideRequestSerializer(data=data)
            if serializer.is_valid(): 
                available_drivers = DriverProfile.objects.filter(latitude__isnull=False, longitude__isnull=False)
                print(available_drivers)
                nearby_drivers = []
                
                for driver in available_drivers:
                    try:
                        driver_distance = haversine_distance(pickup_latitude, pickup_longitude, 
                        float(driver.latitude), float(driver.longitude)
                        )
                        print("driver distance", driver_distance)
                        if driver_distance <= 1.0:  # 1km radius
                            print(driver_distance)
                            nearby_drivers.append(driver)
                            
                    except Exception as e:
                        print(f"Error calculating distance for driver {driver}: {e}")

                print("Nearby drivers within 1km:",nearby_drivers)
                    
                    
                if not nearby_drivers:
                    print("No driver is available...")
                    return Response({"message": "No drivers are available within 1km radius. Please try again later."},status=status.HTTP_200_OK)
                
                # Randomly assign a driver from the nearby drivers
                assigned_driver = random.choice(nearby_drivers)
                
                # Save the ride with the assigned driver
                ride = serializer.save(driver=assigned_driver.user)
                            
                # Send email notification to the driver
                send_ride_email_request(assigned_driver.user.email, ride)
                
                return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)

            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)


# Ride Details Api
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def ride_detail(request, ride_id):
    # if request.user.is_authenticated:
        if request.method == "GET":
            # print(request.user)
            try:
                ride = Ride.objects.get(id=ride_id)
                
            except Ride.DoesNotExist:
                return Response({"error":"Ride not found"} , status=status.HTTP_404_NOT_FOUND)
            
            if request.user != ride.rider and request.user != ride.driver:
                return Response({"error": "You do not have permission to view this ride."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = RideSerializer(ride)
            return Response({"data":serializer.data})
        
        return Response({"error": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    # return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)




# Update Ride Status
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def update_ride_status(request, ride_id):
    # if request.user.is_authenticated:
        if request.method == "PATCH":
            try:
                ride = Ride.objects.get(id=ride_id)
            except Ride.DoesNotExist:
                return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)
            
            if request.user != ride.driver:
                return Response({"error":"you do not have a permision to update this ride."}, status=status.HTTP_403_FORBIDDEN)
                
            data = request.data
            
            allowed_statuses = ['accepted', 'in_progress', 'completed', 'cancelled']
            
            if status in data and data['status'] in allowed_statuses:
                ride.status = data['status']
                ride.save()
                serializer = RideSerializer(ride)
                return Response({"data":serializer.data}, status=status.HTTP_200_OK)
            
            else:
                return Response({"error":"Invalid Status"}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"error":"method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# Cancel Ride Status
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def cancel_ride(request, ride_id):
    # if request.user.is_authenticated:
        if request.method == "PATCH":
            try:
                ride = Ride.objects.get(id=ride_id)
            except Ride.DoesNotExist:
                return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)
            
            if request.user != ride.rider:
                return Response({"error": "You do not have permission to cancel this ride."}, status=status.HTTP_403_FORBIDDEN)
            
            ride.status = "cancelled"
            ride.save()
            serializer = RideSerializer(ride)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# Accept Ride Request API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def accept_ride(request, ride_id):
    # if request.user.is_authenticated:
        if request.method == "POST":
            try:
                ride = Ride.objects.get(id=ride_id, status='requested')
            except Ride.DoesNotExist:
                return Response({"error": "Ride not found or already accepted"}, status=status.HTTP_404_NOT_FOUND)
            
            if request.user != ride.driver:
                return Response({"error": "You do not have permission to accept this ride"}, status=status.HTTP_403_FORBIDDEN)
        
            ride.status = 'accepted'
            ride.save()
            
            # Notify the rider that the ride has been accepted
            send_ride_accepted_email(ride.rider.email, ride)
            
            return Response({"message": "Ride accepted successfully"}, status=status.HTTP_200_OK)

        return Response({"error":"method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
# Reject Ride Request API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def reject_ride(request, ride_id):
    # if request.user.is_authenticated:
        if request.method == "POST":
            try:
                ride = Ride.objects.get(id=ride_id, status='requested')
            except Ride.DoesNotExist:
                return Response({"error": "Ride not found or already processed"}, status=status.HTTP_404_NOT_FOUND)
            
            if request.user != ride.driver:
                return Response({"error": "You do not have permission to reject this ride"}, status=status.HTTP_403_FORBIDDEN)
            
            ride.status = 'rejected'
            ride.save()
            
            # Notify the rider that the ride has been rejected
            send_ride_rejected_email(ride.rider.email, ride)
            
            return Response({"message": "Ride rejected successfully"}, status=status.HTTP_200_OK)
        
        return Response({"error":"method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    
# Rate Ride API.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def rate_ride(request, ride_id):
    # if request.user.is_authenticated:
        if request.method == "POST":
            try:
                ride = Ride.objects.get(id=ride_id, status='completed')
            except Ride.DoesNotExist:
                return Response({'error':"Ride not found or not completed."}, status=status.HTTP_404_NOT_FOUND)
            
            if request.user == ride.rider:
                ride.rider_rating = request.data.get("rider_rating")
                ride.rider_feedback = request.data.get("ride_feedback")
                
            elif request.user == ride.driver:
                ride.driver_rating = request.data.get("driver_rating")
                ride.driver_feedback = request.data.get("driver_feedback")
                
            else:
                return Response({"error": "You do not have permission to rate this ride."}, status=status.HTTP_403_FORBIDDEN)
            
            ride.save()
            return Response({"message": "Rating submitted successfully."}, status=status.HTTP_200_OK)

        return Response({"error":"method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# # Update Driver Location API
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @csrf_exempt
# def update_driver_location(request):
#     # if request.user.is_authenticated:
#         if request.method == "POST":
#             try:
#                 driver_profile = request.user.driver_profile
#                 print(driver_profile)
#             except DriverProfile.DoesNotExist:
#                 return Response({"error":"Driver profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
#             try:
#                 data = request.data
#             except:
#                 return Response({'error':'Data is required.'})    
                
#             serializer = DriverLocationSerializer(data=data)
#             if serializer.is_valid():
#                 driver_profile.latitude = serializer.validated_data['latitude']
#                 driver_profile.longitude = serializer.validated_data['longitude']
#                 driver_profile.save()
#                 return Response({'data':serializer.data}, status=status.HTTP_200_OK)                    
        
#         return Response({"error":"method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    # return Response({'error':"You are not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def rate_ride(request, ride_id):
    # if request.user.is_authenticated:
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user not in [ride.rider, ride.driver]:
            return Response({"error": "You do not have permission to rate this ride."}, status=status.HTTP_403_FORBIDDEN)

        try:
            data = request.data
        except:
            return Response({"error":"Data is required."})
        
        if request.user == ride.rider:
            if 'ride_rating' in data:
                ride.rider_rating = data['rider_rating']
            if 'rider_feedback' in data:
                ride.rider_feedback = data['rider_feedback']
        elif request.user == ride.driver:
            if 'driver_rating' in data:
                ride.driver_rating = data['driver_rating']
            if 'driver_feedback' in data:
                ride.driver_feedback = data['driver_feedback']
                
        ride.save()
        serializer = RideSerializer(ride)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    
    # return Response({'error':'Unauthorized user'}, status=status.HTTP_401_UNAUTHORIZED)