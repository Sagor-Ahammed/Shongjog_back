# messaging/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('<str:recipient>/', message_list, name='message-list'),
    path('thread/<str:recipient>/', message_thread, name='message-thread'),
]
