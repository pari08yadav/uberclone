# import jwt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
import os
from rest_framework_simplejwt.tokens import RefreshToken



# def generate_jwt_token(user):
    
#     payload = {
#         'id': user.id,
#         'username': user.username,
#         'exp' : datetime.now() + timedelta(days=7) 
#     }
#     token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    
#     return token


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }