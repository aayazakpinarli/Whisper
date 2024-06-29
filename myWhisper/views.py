from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def myWhisper(request):
    return HttpResponse("Whisper")


def register(request):
    return render(request, 'register.html')