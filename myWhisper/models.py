from django.db import models
from django.contrib.auth.models import auth, User

# Create your models here.


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50)
    content = models.TextField()
    is_read = models.BooleanField(default=False)


