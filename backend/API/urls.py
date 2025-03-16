from django.contrib import admin
from django.urls import path , include
from .views import *

urlpatterns = [
    path('user-login' , AuthenticationAPI.as_view()) , 
    path('get-candidates' , CandidatesAPI.as_view()) 
]
