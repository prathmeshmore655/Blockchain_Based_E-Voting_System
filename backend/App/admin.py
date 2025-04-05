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



class EtereumModel ( admin.ModelAdmin ) : 


    list_display = [

        "user" ,
        "eth_private_key" ,
        "eth_address" ,
    ]

    search_fields = [
        "user" ,
        "eth_private_key" ,
        "eth_address" ,
    ]
    


admin.site.register(CandidateRegistration , CandidateModel  )
admin.site.register(Voter , VotersModel)
admin.site.register( EthereumAccount , EtereumModel )