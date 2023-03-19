from django.contrib.auth.models import User
from django.db.models import Q

from notifications.models import Notification
from .models import Friend, FriendRequest
from .serializers import FriendSerializer, FriendRequestSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def friend_list(request):
    if request.method == 'GET':
        user = request.user
        friends = Friend.objects.filter(user=user)
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def send_frirnd_request(request, recipient):
    if request.method == 'POST':
        user = request.user
        friend_request = FriendRequest.objects.create(user=user, sent_to=User.objects.get(username=recipient))
        received_from = FriendRequest.objects.create(user=User.objects.get(username=recipient), received_from=user)
        Notification.objects.create(user=User.objects.get(username=recipient),
                                    notification=user.username+' sent you a friend request')
        return Response(status=201)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, recipient):
    if request.method == 'POST':
        user = request.user
        friend = Friend.objects.create(user=user, friends=User.objects.get(username=recipient))
        friend = Friend.objects.create(user=User.objects.get(username=recipient), friends=user)
        friend_request = FriendRequest.objects.filter(user=user, received_from=User.objects.get(username=recipient))
        friend_request.delete()
        friend_request = FriendRequest.objects.filter(user=User.objects.get(username=recipient), sent_to=user)
        friend_request.delete()
        Notification.objects.create(user=User.objects.get(username=recipient),
                                    notification=user.username+' accepted your friend request')
        return Response(status=201)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def friend_request_list(request):
    if request.method == 'GET':
        user = request.user
        friend_requests = FriendRequest.objects.filter(user=user)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfriend(request, recipient):
    if request.method == 'POST':
        user = request.user
        friend = Friend.objects.filter(user=user, friends=User.objects.get(username=recipient))
        friend.delete()
        friend = Friend.objects.filter(user=User.objects.get(username=recipient), friends=user)
        friend.delete()
        return Response(status=201) # return Response

