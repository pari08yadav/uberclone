from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import RideSerializer
from .models import Ride
from users.models import DriverProfile
from django.views.decorators.csrf import csrf_exempt
from email_send import send_ride_email_request, send_ride_rejected_email, send_ride_accepted_email

# Create Ride API
@api_view(['POST'])
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



# Request Ride API
@api_view(['POST'])
@csrf_exempt
def request_ride(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            serializer = RideSerializer(data=request.data)
            
            if serializer.is_valid(): 
                available_drivers = DriverProfile.objects.all()
                if not available_drivers.exists():
                    return Response({"error": "No drivers available"}, status=status.HTTP_400_BAD_REQUEST)
                
                assigned_driver = available_drivers.first()

                if assigned_driver:
                    ride['driver'] = assigned_driver.id
                
                ride = serializer.save(rider = request.user, driver=assigned_driver.user)
                
                # send mail to driver for ride request
                send_ride_email_request(assigned_driver.user.email, ride)
                
                return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)

            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# Ride Details Api
@api_view(['GET'])
@csrf_exempt
def ride_detail(request, ride_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            print(request.user)
            try:
                ride = Ride.objects.get(id=ride_id)
            except Ride.DoesNotExist:
                return Response({"error":"Ride not found"} , status=status.HTTP_404_NOT_FOUND)
            
            if request.user != ride.rider and request.user != ride.driver:
                return Response({"error": "You do not have permission to view this ride."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = RideSerializer(ride)
            return Response({"data":serializer.data})
        
        return Response({"error": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)




# Update Ride Status
@api_view(['PATCH'])
@csrf_exempt
def update_ride_status(request, ride_id):
    if request.user.is_authenticated:
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
@csrf_exempt
def cancel_ride(request, ride_id):
    if request.user.is_authenticated:
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
@csrf_exempt
def accept_ride(request, ride_id):
    if request.user.is_authenticated:
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
@csrf_exempt
def reject_ride(request, ride_id):
    if request.user.is_authenticated:
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
@csrf_exempt
def rate_ride(request, ride_id):
    if request.user.is_authenticated:
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
    


