from urllib import request

from django.shortcuts import render, redirect
from myWhisper.models import Users, Message
from django.contrib import messages
from django.contrib.auth.models import auth


# Create your views here.


def myWhisper(request):
    return render(request, 'index.html')

def login(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):

    if request.method == 'POST':
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        if password != confirm_password:
            messages.info(request, 'Passwords must match!')
        else:
            email = request.POST['email']
            if Users.objects.filter(email=email).exists():
                messages.info(request, 'Email exists!')
            else:
                username = request.POST['username']
                if Users.objects.filter(username=username).exists():
                    messages.info(request, 'Username exists!')
                else:
                    first_name = request.POST['name']
                    last_name = request.POST['surname']
                    user = Users(name=first_name, last_name=last_name,
                                 email=email, username=username, password=password)
                    try:
                        user.save()
                        print("User saved successfully!")
                        return redirect('login')
                    except Exception as e:
                        print(f"Error saving user: {str(e)}")
                        messages.info(request, 'Save errorr!!')

        return render(request, 'register.html')
    else:
        return render(request, 'register.html')
