# messaging/views.py

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Message
from .serializers import MessageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def message_list(request, recipient):
    if request.method == 'GET':
        user = request.user
        messages = Message.objects.filter(sender=user, recipient__username=recipient)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, recipient=User.objects.get(username=recipient))
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# chat/views.py

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_thread(request, recipient):
    user = request.user
    messages = Message.objects.filter(
        (Q(sender=user) & Q(recipient__username=recipient)) |
        (Q(sender__username=recipient) & Q(recipient=user))
    ).order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

