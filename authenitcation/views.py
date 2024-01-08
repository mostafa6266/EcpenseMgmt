from django.shortcuts import render , redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages , auth
# from django.core.mail import EmailMultiAlternatives, get_connection, EmailMessage
import json
# Create your views here.




class EmailValidationViwe(View):
    def post(self , request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_erorr' : 'Email is invalid'} , status = 400)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_erorr' : 'sorry email in use , choose another one'} , status = 409)
        return JsonResponse({'email_valid':True}) 

class UsernameValidationViwe(View):
    def post(self , request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_erorr' : 'username should only contain alphanumeric characters'} , status = 400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_erorr' : 'sorry username in use , choose another one'} , status = 409)
        
        return JsonResponse({'username_valid':True}) 
class RegistrationViwe(View):
    def get(self , request):
        return render (request , 'authenitcation/register.html' )
    
    def post(self , request):
        #Get User Data
        username = request.POST['username']  
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues':request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request , 'Password to short')
                    return render (request , 'authenitcation/register.html', context )
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                # connection = get_connection()  # Call the function to get a connection instance
                # connection.open()

                # email_subject = 'Activate your account'
                # user_email = request.POST['email']  # Make sure you get the email from the form
                # email_body = 'Hi '+ user.username + ', Please the link below to activate your account '

                # email = EmailMessage(
                #     email_subject,
                #     email_body,
                #     'noreply@semycolon.com',
                #     [user_email],
                # )
                # email.connection = connection  # Use the connection you opened
                # email.send(fail_silently=False)

                # connection.close()

                messages.success(request, 'Account Successfully Created')
                return redirect('login')
  
            
        return render (request , 'authenitcation/register.html' )
    
    
class LoginView(View):
    def get(sels , request):
        return render(request , 'authenitcation/login.html')    

    def post(self , request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password :
            user = auth.authenticate(username = username , password = password)
            if user:
                if user.is_active:
                    auth.login(request , user)
                    messages.success(request , f'Welcome {user.username} You are now logged in')
                    return redirect('expenses')
                messages.error(request , 'Account in not active , Please contact the admin')
                return render(request , 'authenitcation/login.html')
        messages.error(request , 'Invalid credentials , Try again')
        return render(request , 'authenitcation/login.html')        


class LogoutView(View):
    def post(self , request):
        auth.logout(request)
        messages.success(request , 'You have been logged out')
        return redirect('login')