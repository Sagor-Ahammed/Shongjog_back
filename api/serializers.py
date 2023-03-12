from .models import Post, Comment, Like, profile_picture
from rest_framework import serializers
from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ['user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at', 'likes']


class profile_pictureSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = profile_picture
        fields = ['user', 'image']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True, allow_null=True)
    likes = LikeSerializer(many=True, read_only=True, allow_null=True)
    image = serializers.ImageField(max_length=None, use_url=True, required=False,allow_null=True)
    video = serializers.FileField(max_length=None, use_url=True, required=False,allow_null=True)


    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'video', 'created_at', 'comments', 'likes']


