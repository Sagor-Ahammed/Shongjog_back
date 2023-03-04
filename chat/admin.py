from .models import Message

from django.contrib import admin

#register the model with the admin site
admin.site.register(Message)