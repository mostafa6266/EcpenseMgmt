from django.urls import path
from .views import RegistrationViwe , UsernameValidationViwe , EmailValidationViwe , LoginView , LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register' , RegistrationViwe.as_view() , name='register'),
    path('login' , LoginView.as_view() , name='login'),
    path('logout' , LogoutView.as_view() , name='logout'),
    path('validate-username' ,csrf_exempt( UsernameValidationViwe.as_view() ), name='validate-username'),
    path('validate-email', csrf_exempt (EmailValidationViwe.as_view()) , name='validate-email'),
]


#authenitcation