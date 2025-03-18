from django.contrib import admin
from .models import *
# Register your models here.


class CandidateModel (admin.ModelAdmin) : 

    list_display = [
        "candidate_id" ,
        "name" ,
        "party" ,
        "age" ,
        "bio" ,
        "photo" ,
        "election_position" ,
        "created_at" ,
        "election_sign" 
    ]

    search_fields = [
        "candidate_id" ,
        "name" ,
        "party" ,
        "age" ,
        "bio" ,
        "photo" ,
        "election_position" ,
        "created_at" ,
        "election_sign" 
    ]



class VotersModel (admin.ModelAdmin) : 

    list_display = [
        "user",
        "voter_id",
        "created_at",
        "is_voted"
    ]

    search_fields = [
        "user",
        "voter_id",
        "created_at",
        "is_voted"
    ]
    


admin.site.register(CandidateRegistration , CandidateModel  )
admin.site.register(Voter , VotersModel)