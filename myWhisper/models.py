from django.db import models
from django.contrib.auth.models import User
# Utility class for creating complex queries, allowing OR, AND operations
from django.db.models import Q

# Create your models here.


class ThreadManager(models.Manager):
    # kwargs: allow passing keyword arguments; here, it expects user
    def get_threads_by_user(self, **kwargs):
        user = kwargs.get('user')
        # construct query condition that checks if the user is either first_person or second_person in thread
        # where first_person = user , | logical OR
        lookup = Q(first_person=user) | Q(second_person=user)
        # take all thread records , match the conditions specified by lookup (user f_p or s_p),
        # ensure that qs returns unique records (SELECT DISTINCT)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    # cascade delete related items on the foreign key
    # related_name : thread üzerinden thread_first_person'a ulaşılabilir kılıyor
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_first_person')
    # thread_as_first_person = user.thread_second_person olarak kullanılabilir
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='thread_second_person')
    # auto_now : every time the object saved, set the field to the current timestamp
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add : when the object created, sets the field to the current timestamp
    # timestamp: tarih bilgisi
    timestamp = models.DateTimeField(auto_now_add=True)

    # assign a custom manager 'threadManager' to the model,
    # allowing you to add custom query methods (like by_user) to the 'thread' model
    objects = ThreadManager()

    # This constraint ensures that each pair of users has at most one unique thread
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    # null=true : allows this fields to be null in database, a message can exist without being associated w thread
    # blank=true : allow this field to be empty in forms
    # related_name :
    thread = models.ForeignKey(Thread, null=True, blank=True,
                               related_name='chatmessage_thread', on_delete=models.CASCADE)
    # cascade : protect (prevent deletion of the referenced obj by raising ProtectedError), set_null,
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='host_user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

