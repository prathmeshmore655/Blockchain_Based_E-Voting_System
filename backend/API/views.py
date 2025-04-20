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
from django.core.mail import send_mail
import random
from django.conf import settings




    



class CandidatesAPI (APIView) : 


    permission_classes = [AllowAny]

    def get(self, request):
        data = CandidateRegistration.objects.all()
        s_data = CandidateSerializers(data, many=True)
        return JsonResponse(s_data.data, safe=False)
    

class SendOTPAPI ( APIView ) : 


    def get ( self , request ) : 

        return Response({"message" : "hello"}  , status = status.HTTP_200_OK) 

    def post ( self , request ) : 

        data = json.loads(request.body)
        email = data.get('email')

        b_otp = random.randint( 100000 , 999999 )
        request.session['otp'] = b_otp
        request.session['email'] = email

        send_mail(
          subject='Your OTP Code',
            message=f'Your OTP is: {b_otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )


        return Response({'message' : "Otp  send successfully "} , status=status.HTTP_200_OK)


