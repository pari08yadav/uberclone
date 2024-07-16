from django.conf import settings
from .models import Payment
from .serializer import PaymentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from ride.models import Ride
import stripe

# Create your views here.


@api_view(['POST'])
@csrf_exempt
def create_payment_intent(request):
    # if request.user.is_authenticated:
    if request.method == "POST":
        try:
            ride = Ride.objects.get(id=request.data.get('ride_id'))
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != ride.rider:
            return Response({"error": "You do not have permission to pay for this ride."}, status=status.HTTP_403_FORBIDDEN)

        amount = int(ride.fare * 100)
        
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                metadata={'integration_check': 'accept_a_payment'},
            )
        except Exception as e:
            return Response({"error":e})
        
        payment = Payment.objects.create(
            ride=ride,
            amount=ride.fare,
            stripe_payment_intent_id=payment_intent['id'],
            status='pending',
        )
        
        if payment:
            return Response({
                'payment_intent': payment_intent,
                'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
            })
            


@api_view(['POST'])
@csrf_exempt
def confirm_payment(request):
    payment_id = request.data.get('payment_id')
    payment_intent_id = request.data.get('payment_intent_id')
    
    try:
        payment = Payment.objects.get(id=payment_id, stripe_payment_intent_id=payment_intent_id)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)


    if request.user != payment.ride.rider:
        return Response({"error": "You do not have permission to confirm this payment."}, status=status.HTTP_403_FORBIDDEN)

    try:
        stripe.PaymentIntent.confirm(payment_intent_id)
        payment.status = 'completed'
        payment.save()
        return Response({"message": "Payment confirmed successfully."})
    except stripe.error.StripeError as e:
        payment.status = 'failed'
        payment.save()
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

