from django.contrib import admin
from django.urls import path , include
from .views import *

urlpatterns = [
    path('get-candidates' , CandidatesAPI.as_view()) ,
    path('send-otp' , SendOTPAPI.as_view() , name = "send-otp")
]
