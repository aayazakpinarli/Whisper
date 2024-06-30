from django.shortcuts import render, redirect
from myWhisper.models import Users, Message
from pyexpat.errors import messages


# Create your views here.


def myWhisper(request):
    return render(request, 'index.html')


def register(request):

    if request.method == 'POST':
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        if password != confirm_password:
            messages.error(request, 'Passwords must match')
        else:
            email = request.POST['email']
            if Users.objects.filter(email=email).exists():
                messages.error(request, 'Email exists')
            else:
                username = request.POST['username']
                if Users.objects.filter(username=username).exists():
                    messages.error(request, 'Username exists')
                else:
                    first_name = request.POST['name']
                    last_name = request.POST['surname']
                    user = Users(name=first_name, last_name=last_name,
                                 email=email, username=username, password=password)
                    try:
                        user.save()  # Save the user object to the database
                        print("User saved successfully!")
                    except Exception as e:
                        print(f"Error saving user: {str(e)}")
                    return redirect('/')
    else:
        return render(request, 'register.html')

