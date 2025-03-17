from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import CandidateSerializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from App.models import *
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
import json






    



class CandidatesAPI (APIView) : 

    def get(self, request):


        data = CandidateRegistration.objects.all()

        print("data" , data)

        s_data = CandidateSerializers(data, many=True)
        return Response(s_data.data, status=status.HTTP_200_OK)
