from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import CandidateSerializers
from django.http import JsonResponse
from App.models import *
import json

class AuthenticationAPI (APIView) : 

    def post (self , request)  :

        data = request.data

        username = data.get('username')
        password = data.get('password')
        # voter_no = data.get('voter_no')

        user = authenticate(username = username , password = password )
        # vote = Voters_Table.objects.get( card_no  = voter_no)
        
        if user : 

            login (request , user)

            return Response({"message" : "User successfully log in "} , status=status.HTTP_200_OK)
        else : 

            return Response({"message" : "Enter Valid Credentials"} , status=status.HTTP_404_NOT_FOUND)





class CandidatesAPI (APIView) : 

    def get(self, request):


        data = CandidateRegistration.objects.all()

        print("data" , data)

        s_data = CandidateSerializers(data, many=True)
        return Response(s_data.data, status=status.HTTP_200_OK)
