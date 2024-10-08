from django.urls import path
from .views import MessagesPageView, LoginView, LogoutView, RegisterView, AddFriendView, ProfileView, VerifyMailView

urlpatterns = [
    path('', MessagesPageView.as_view(), name='messagesPage'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyMailView.as_view(), name='verify'),
    path('addFriend/', AddFriendView.as_view(), name='addFriend'),
    path('profile/', ProfileView.as_view(), name='profile'),

]
