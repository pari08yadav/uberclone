from django.contrib import admin
from django.urls import path
from ride import views

urlpatterns = [
    path('create_ride/', views.create_ride, name="create_ride"),
    # path('get_ride/<int:ride_id>/', views.get_ride, name="get_ride"),
    path('update_ride/<int:ride_id>/', views.udpate_ride, name="update_ride"),
    path('list_rides/<int:ride_id>/', views.list_rides, name="list_rides"),
    path('delete_ride/<int:ride_id>/', views.delete_ride, name="delete_ride"),
    path('request_ride/', views.request_ride, name="request_name"),
    path('geocode_address/', views.geocode_address, name="geocode_address"),
    path('autocomplete_address/', views.autocomplete_address, name="autocomplete_address"),
    # path('place_Search/', views.place_search, name="place_search"),
    path('ride_detail/<int:ride_id>/', views.ride_detail, name="ride_detail"),
    path('update_ride_status/<int:ride_id>/', views.update_ride_status, name="update_ride_status"),
    path('cancel_ride/<int:ride_id>/', views.cancel_ride, name="cancel_ride"),
    path('accept_ride/<int:ride_id>/',views.accept_ride, name="accept_ride"),
    path('reject_ride/<int:ride_id>/', views.reject_ride, name="reject_ride"),
    path('rate_ride/<int:ride_id>/', views.rate_ride, name="rate_ride"),
    # path('update_driver_location/', views.update_driver_location, name="update_driver_location")
]