from django.shortcuts import redirect, render
from App.models import *

def login_page(request) : 

    return render (request , 'login.html')


    
def home_page (request) :


    return render (request , 'home.html')
    


def vote_page (request) :


   

        print("user login" , request.user.id)
        user = request.user.id
        return render (request , 'vote.html' , {'user' : user})
    

def elections_page (request ):
     
     return render (request , 'elections.html')


def dashboard_page(request ) : 
     
     candidates = CandidateRegistration.objects.all()
     
     return render (request , 'dashboard.html')