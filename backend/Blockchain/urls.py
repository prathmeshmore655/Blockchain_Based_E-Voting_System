from django.contrib import admin
from django.urls import path , include
from .views import *

urlpatterns = [
    path('blockchain-api' , BlockchainAPI.as_view() ),
    path('fetch-candidates' , CandidatesAPI.as_view()),
    # path('fetch-candidates-blockchain' , )
    
]
