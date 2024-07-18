from django.contrib import admin
from .models import Thread, ChatMessage
from django.core.exceptions import ValidationError
from django import forms


# Register your models here.

# allows ChatMessage instance to be managed through admin interface
admin.site.register(ChatMessage)


# allow for inline editing ChatMessage within another model's admin interface
# tabularInline: django admin class that displays related models in tabular format (as rows)
# within the parent model's admin page
class ChatMessageInline(admin.TabularInline):
    model = ChatMessage


'''class ThreadForm(forms.ModelForm):
    def clean(self):
        """
        This is the function that can be used to
        validate your model data from admin
        """
        super(ThreadForm, self).clean()
        first_person = self.cleaned_data.get('first_person')
        second_person = self.cleaned_data.get('second_person')
        lookup1 = Q(first_person=first_person) & Q(second_person=second_person)
        lookup2 = Q(first_person=second_person) & Q(second_person=first_person)
        lookup = Q(lookup1 | lookup2)
        qs = Thread.objects.filter(lookup)
        if qs.exists():
            raise ValidationError(f'Thread between {first_person} and {second_person} already exists.')
'''


# inherits from admin.ModelAdmin, allows customization of how the Thread model is displayed and managed
# in the Django admin interface
# THIS IS FOR CUSTOMIZATION
class ThreadAdmin(admin.ModelAdmin):
    # inlines: specifies that instances of ChatMessage should be displayed inline within the Thread admin page
    # using chatMessageInline allows user to view and edit related ChatMessage entries directly on thread admin page
    inlines = [ChatMessageInline]

    class Meta:
        # associate threadAdmin class with Thread model. It tells Django
        # that this admin class is meant to manage Thread instances
        model = Thread


# register thread model with Django admin site
# THIS IS FOR REGISTRATION
# it tells Django to use ThreadAdmin class to manage how the Thread model appears in the admin interface
admin.site.register(Thread, ThreadAdmin)
