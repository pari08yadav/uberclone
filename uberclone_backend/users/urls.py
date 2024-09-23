from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('user_list/', views.user_list, name="user_list"),
    path('update_user_profile_picture/', views.update_user_profile_picture, name="update_user_profile_picture"),
    path('user_profile_update/', views.user_profile_update, name="user_profile_update"),
    path('user_details/', views.user_details, name="user_details"),
    path('user_delete', views.user_details, name="user_details"),
    path('password_reset/', views.password_reset_request, name="password_reset_request"),
    path('password_reset_confirm/<token>/', views.password_reset_confirm, name="password_reset_confirm"),
    path('update_driver_location/', views.update_driver_location, name="update_driver_location"),
    path('create_driver_profile/', views.create_driver_profile, name="create_driver_profile"),
    path('check_driver_profile/', views.check_driver_profile, name="check_driver_profile"),
    path('get_driver_profile/', views.get_driver_profile, name="get_driver_profile"),
    path('driver-profile/update/put/', views.update_driver_profile, name="update_driver_profile"),
    path('driver-profile/update/patch/', views.update_driver_profile_partially, name="update_driver_profile_partially"),
]