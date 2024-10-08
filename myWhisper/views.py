from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from myWhisper.models import Thread
from django.views import View
from django.utils.decorators import method_decorator
from .utils import generate_random_number
from django.core.mail import send_mail


# Create your views here.


@method_decorator(login_required, name='dispatch')
# view inherited
class MessagesPageView(View):
    def get(self, request):

        threads = (Thread.objects.get_threads_by_user(user=request.user)
                   .prefetch_related('chatmessage_thread').order_by('timestamp'))


        # DELETE FOR USE ORM
        # CREATE ADDFRIEND VIEW
        # CAN BE USED VALUE LIST TO HIT ONCE

        not_added_friends = []
        already_added_friends = [request.user]
        for thread in threads:
            if thread.first_person == request.user:
                already_added_friends.append(thread.second_person)
            elif thread.second_person == request.user:
                already_added_friends.append(thread.first_person)

        users = User.objects.all()
        for user in users:
            if not user in already_added_friends:
                not_added_friends.append(user)
        print(not_added_friends)
        #print(users - already_added_friends)
        # a context disc is created, includes threads query set
        # this context will be passed to the template for rendering
        context = {
            'Threads': threads,
            'Friends': not_added_friends
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
        password1 = request.POST['password1']
        confirm_password = request.POST['password2']
        if password1 != confirm_password:
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
                                                    email=email, username=username, password=password1, is_active=False)

                    generated_code = generate_random_number()
                    content = 'Your verification code is : ' + str(generated_code)
                    send_mail(
                        "MyWhisper Registeration",
                        content,
                        'mywhisperinf@gmail.com',
                        [user.email],
                    )

                    print("message send w", generated_code)
                    try:
                        print(user.id)
                        user.save()
                        request.session['registered_user_id'] = user.id
                        request.session['generated_code'] = generated_code

                        return redirect('verify')

                    except Exception as e:
                        print(f"Error saving user: {str(e)}")
                        messages.info(request, 'Error!!')
                        return redirect('login')


class VerifyMailView(View):
    def get(self, request):
        return render(request, 'verify_email.html')

    def post(self, request):

        # CODE CAN BE ADDED TO THE DATABASE
        # ADD MAX TIME FOR GENERATED CODE

        try:
            user_id = request.session.get('registered_user_id')
            if not user_id:
                messages.info(request, 'No user information found.')
                return redirect('/')

            print(user_id)
            user = User.objects.get(id=user_id)

            code = request.POST['code']
            generated_code = request.session.get('generated_code')
            print(code)
            print(user)
            if code == str(generated_code):
                user.is_active = True
                user.save()
            else:
                return redirect('/')
        except Exception as e:
            print(f"Error saving user: {str(e)}")
            messages.info(request, 'Error!!')

        return redirect('login')


class AddFriendView(View):
    def post(self, request):
        friend_id = request.POST.get('friend_id')
        friend = User.objects.filter(id=friend_id)
        Thread.objects.create(first_person=request.user, second_person=friend[0])

        return redirect('/')


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

        if old_password and new_password:
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
