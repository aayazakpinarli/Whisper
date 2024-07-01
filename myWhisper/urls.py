from django.urls import path
from . import views

urlpatterns = [
    path('', views.myWhisper, name='myWhisper'),
    path('register/', views.register, name='register'),

]