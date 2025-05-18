from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from App.models import *
import json
from django.contrib.auth import authenticate, login
import random
from django.core.mail import send_mail



def login_page(request) : 

    return render (request , 'login.html')


    
def home_page (request) :


    return render (request , 'home.html')
    


def vote_page (request) :
     
        user = request.user.id
        return render (request , 'vote.html' , {'user' : user})
    

def elections_page (request ):
     
     return render (request , 'elections.html')


def dashboard_page(request ) : 
     
     
     return render (request , 'dashboard.html')


def contact_us_page (request ) : 
     
     return render (request , 'contact.html')


def working_page (request ) : 
     
     return render ( request , 'working.html')

def create_account ( request ) : 

     return render( request , 'create_account.html')





def user_login (request)  :


        username = request.POST.get('username') 
        password = request.POST.get('password')
        voter_no = request.POST.get('voter_no')

        user = authenticate(username = username , password = password )

        try :

          vote = Voter.objects.get( voter_id = voter_no)

        except : 
             
          return render(request , 'login.html' , {"message" : "Enter valid Voter ID"}  )
        
        if user and vote:
                
                login(request, user)

                return redirect('home_page')
        else : 

            return render(request , 'login.html' , {"message" : "Enter valid credentials"}  )
        



def validate_otp ( request ) : 

     data = json.loads(request.body)
     otp = data.get('otp')

     b_otp = request.session.get('otp')
     email = request.session.get('email')

     request.session.pop('otp')
     request.session.pop('email')

     print(otp)
     print(b_otp)

     if int(otp) == int(b_otp) : 

          return JsonResponse({'message' : "Otp matched Successfully" , 'status' : "success"} )
     else : 

          return JsonResponse({'message' : "incoorrect otp" , 'status' : "fail"})




def register_user( request ) : 

     username = request.POST.get('username')
     email = request.POST.get('email')
     voter_id = request.POST.get('voter_id')
     password = request.POST.get('password')


     user = User.objects.create( username = username , email = email)
     user.set_password(password)
     user.save()

     voter = Voter.objects.create( user = user , voter_id = voter_id  )
     voter.save()

     return redirect(login_page)

     