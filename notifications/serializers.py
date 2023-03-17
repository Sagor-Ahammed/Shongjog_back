from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Notification
from django.contrib import admin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ('id', 'notification', 'user')

