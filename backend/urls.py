from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('API/' , include('API.urls')),
    path('Blockchain/' ,include('Blockchain.urls')),
    path('' , views.login_page , name = "login_page") ,
    path('create_account' , views.create_account , name = "create_account") ,
    path('home' , views.home_page , name = "home_page") ,
    path('vote' , views.vote_page , name = "vote_page"),
    path('elections' , views.elections_page , name = "elections_page") ,
    path('dashboard' , views.dashboard_page , name = "dashboard_page"),
    path('working' , views.working_page , name = "working_page"),
    path('contact' , views.contact_us_page , name = "contact_us_page") , 
    path('user_login' , views.user_login , name = "user_login"),
    path('register_user' , views.register_user , name = "register_user")  ,
    path('validate_otp' , views.validate_otp , name  = "validate_otp") ,

]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

