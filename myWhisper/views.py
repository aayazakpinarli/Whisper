from urllib import request

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from myWhisper.models import Thread
from django.views import View
from django.utils.decorators import method_decorator

# Create your views here.


@method_decorator(login_required, name='dispatch')
class MessagesPageView(View):
    def get(self, request):
        threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
        context = {
            'Threads': threads
        }
        return render(request, 'chat/messages.html', context)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('login')



class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('login')

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        if password != confirm_password:
            messages.info(request, 'Passwords must match!')
        else:
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email exists!')
            else:
                username = request.POST['username']
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username exists!')
                else:
                    first_name = request.POST['name']
                    last_name = request.POST['surname']
                    user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                                    email=email, username=username, password=password)
                    try:
                        user.save()
                        print("User saved successfully!")

                        # Create threads with all existing users
                        existing_users = User.objects.exclude(id=user.id)
                        for existing_user in existing_users:
                            Thread.objects.create(first_person=user, second_person=existing_user)
                        print("Threads created successfully!")

                        return redirect('login')
                    except Exception as e:
                        print(f"Error saving user: {str(e)}")
                        messages.info(request, 'Error!!')
        return render(request, 'register.html')
