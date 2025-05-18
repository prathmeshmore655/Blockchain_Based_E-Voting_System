from rest_framework.serializers import ModelSerializer
from App.models import *


class CandidateSerializer (ModelSerializer) : 

    class Meta : 

        model =  CandidateRegistration
        fields = '__all__'