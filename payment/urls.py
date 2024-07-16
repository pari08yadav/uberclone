from payment import views
from django.urls import path

urlpatterns = [
    path('create_payment_intent/', views.create_payment_intent, name='create_payment_intent'),
    path('confirm_payment/', views.confirm_payment, name="confirm_payment")
]