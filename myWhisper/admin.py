from django.contrib import admin
from .models import Users
from .models import Message

# Register your models here.
admin.site.register(Users)
admin.site.register(Message)