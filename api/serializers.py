from rest_framework import serializers
from .models import Post, Comment, Like

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

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'created_at', 'comments', 'likes']
