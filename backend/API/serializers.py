from rest_framework.serializers import ModelSerializer
from App.models import *




class CandidateSerializers (ModelSerializer) : 

    class Meta : 

        model = CandidateRegistration
        fields = '__all__'