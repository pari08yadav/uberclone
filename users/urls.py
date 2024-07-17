from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('user_list/', views.user_list, name="user_list"),
    path('user_details/', views.user_details, name="user_details"),
    path('user_delete', views.user_details, name="user_details"),
    path('password_reset/', views.password_reset_request, name="password_reset_request"),
    path('password_reset_confirm/<token>', views.password_reset_confirm, name="password_reset_confirm"),
    path('create_driver_profile/', views.create_driver_profile, name="create_driver_profile"),
    path('get_driver_profile/', views.get_driver_profile, name="get_driver_profile"),
    path('driver-profile/update/put/', views.update_driver_profile, name="update_driver_profile"),
    path('driver-profile/update/patch/', views.update_driver_profile_partially, name="update_driver_profile_partially"),
    path('update_driver_location/', views.update_driver_location, name="update_driver_location")
]