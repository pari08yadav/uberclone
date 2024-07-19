from django.urls import path
from .consumers import DriverLocationConsumer

websocket_urlpatterns = [
    path('ws/driver/<int:driver_id>/', DriverLocationConsumer.as_asgi()),
]
