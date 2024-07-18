from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from myWhisper.models import Thread
from django.views import View
from django.utils.decorators import method_decorator

# Create your views here.


# ensure that only authenticated users can access this page
# dispatch: it will affect all HTTP methods like GET, POST
@method_decorator(login_required, name='dispatch')
# view inherited
class MessagesPageView(View):
    def get(self, request):
        # calls the custom manager method 'by_user', which retrieves all Thread instances
        # where the logged-in user is either first_p or second_person
        # prefetch: optimizing technique that fetches related chatMessage instances in a single query, instead of
        # increasing num of hits to the db, in single query I can collect all the messages
        # order_by (ORDER BY)
        threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
        # a context disc is created, includes threads query set
        # this context will be passed to the template for rendering
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


class AddFriendView(View):
    def get(self, request):
        return render(request, 'chat/addFriend.html')


class ProfileView(View):
    def get(self, request):
        return render(request, 'chat/profile.html')

    def post(self, request):
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        user = request.user

        if username:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username exists!')
            else:
                user.username = username
                user.save()
                return redirect('/')

        if old_password:
            if new_password:
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    return redirect('/')
                else:
                    messages.info(request, 'Old password is incorrect!')
            else:
                messages.info(request, 'Please enter new password!')

        if not old_password and not new_password and not username:
            messages.info(request, 'Please fill!')

        return redirect('/profile')
