from django.urls import path
from myWhisper import views as chat_views
from . import views

urlpatterns = [
    path("", views.messagesPage),
    #path('', views.myWhisper, name='myWhisper'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
