from django.urls import path
from .views import *

urlpatterns = [
    path('', friend_list, name='friend_list'),
    path('friend-request/send/<str:recipient>/', send_frirnd_request, name='send_friend_request'),
    path('friend-request/accept/<str:recipient>/', accept_friend_request, name='accept_friend_request'),
    path('friend-requests/', friend_request_list, name='friend_request_list'),
    path('unfriend/<str:recipient>/', unfriend, name='unfriend'),
]
