from django.core.mail import send_mail
from django.conf import settings


def send_ride_email_request(user_email, ride):
    subject = f"New Ride Request from {ride.rider.username}"
    message = f"You have a new ride request. Details:\n\nPickup Location: {ride.pickup_location}\nDropoff Location: {ride.drop_location}\nCreatedAt: {ride.created_at}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
    


def send_ride_accepted_email(rider_email, ride):
    subject = 'Your Ride Request Has Been Accepted'
    message = f"""
    Dear {ride.rider.username},

    Your ride request has been accepted by {ride.driver.user.username}. Here are the details of your ride:

    Driver Name: {ride.driver.user.username}
    License Number: {ride.driver.license_number}
    Vehicle Type: {ride.driver.vehicle_type}
    Vehicle Registration Number: {ride.driver.vehicle_registration_number}
    Years of Experience: {ride.driver.years_of_experience}

    You can contact the driver at: {ride.driver.user.email}

    Thank you for using our service.

    Best regards,
    Uber Clone Team
    """

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [rider_email])



def send_ride_rejected_email(rider_email, ride):
    subject = 'Your Ride Request Has Been Rejected'
    message = f"""
    Dear {ride.rider.username},

    Unfortunately, your ride request has been rejected by {ride.driver.user.username}. 

    Please try requesting another ride.

    Thank you for using our service.

    Best regards,
    Uber Clone Team
    """

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [rider_email])