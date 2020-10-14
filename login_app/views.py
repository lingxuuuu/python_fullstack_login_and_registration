from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def success(request):
    if 'user_id' not in request.session: 
    #'user_id' is from session
        return redirect('/')
    print(request.POST)
    return render(request, 'dashboard.html')

def register_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash messagecopy
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        #hashes the password
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print('hash password: ', hash_password)
        #create a new user
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'], 
            email=request.POST['email'], 
            #password=request.POST['password] we do not want to store the pw directly into the db
            password=hash_password,
            )
        print('New user password: ',new_user.password)
        #setup session
        request.session['user_id'] = new_user.id
    return redirect('/success')   
    #return redirect(f'/success/{new_user.id}')

def login_user(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash messagecopy
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:  
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/success')
      

def logout(request):
    print(request.POST)
    print("Logging out")
    request.session.flush()
    return redirect('/')   