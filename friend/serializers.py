from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Friend, FriendRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class FriendSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    friends = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Friend
        fields = ['id', 'user', 'friends']

class FriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    sent_to = serializers.StringRelatedField(read_only=True)
    received_from = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'user', 'sent_to', 'received_from']

