from django.shortcuts import redirect, render
from App.models import *
import json
from django.contrib.auth import authenticate, login


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


def contact_us_page (request ) : 
     
     return render (request , 'contact.html')


def working_page (request ) : 
     
     return render ( request , 'working.html')







def user_login (request)  :


        username = request.POST.get('username') 
        password = request.POST.get('password')
        # voter_no = data.get('voter_no')

        user = authenticate(username = username , password = password )
        # vote = Voters_Table.objects.get( card_no  = voter_no)
        
        if user:
                
                login(request, user)

                print("Session Key:", request.session.session_key)  # Debugging
                
                return redirect('home_page')
        else : 

            return (request , {"message" : "Enter Valid Credentials"} )

