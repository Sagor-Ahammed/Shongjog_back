import json
from difflib import SequenceMatcher
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from rest_framework import status, generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, SAFE_METHODS, BasePermission
from rest_framework.response import Response
from .models import Post, Comment, Like, profile_picture
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, UserSerializer, RegisterSerializer, profile_pictureSerializer
from knox.models import AuthToken
from django.contrib.auth.models import User
from django.http import JsonResponse


from knox.views import LoginView as KnoxLoginView 
from django.contrib import admin

admin.site.site_header = "ShongJok"
admin.site.site_title = "Shongjok"
admin.site.index_title = "Welcome to Shongjuk"


class IsOwnerOrChangePostPermission(BasePermission):
    """
    Custom permission to allow post owner and users with change_post permission to modify comments and likes.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET requests for all users
        if request.method in SAFE_METHODS:
            return True

        # Allow modification only if user is the owner of the post or has the 'change_post' permission
        return obj.post.author == request.user or request.user.has_perm('change_post', obj.post)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


#posts
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def post_list_create_api_view(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, image=request.data.get('image', None), video=request.data.get('video', None))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(['PUT', 'DELETE', 'GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail_api_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'PUT' and post.author == request.user:
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE' and post.author == request.user:
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    return Response(status=status.HTTP_403_FORBIDDEN)


#comments
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly, IsOwnerOrChangePostPermission])
def create_comment_api_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=404)

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(post=post, author=request.user)
        post.comments.add(serializer.instance)
        post.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, IsOwnerOrChangePostPermission])
def comment_detail_api_view(request, post_id, pk):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if comment.author != request.user:
            return Response({"error": "You do not have permission to delete this comment."}, status=403)
        comment.delete()
        post.comments.remove(comment)
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(author=request.user, post=post)
            post.comments.append(comment)
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)



#likes
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def like_list_create_api_view(request):
    if request.method == 'GET':
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated, IsOwnerOrChangePostPermission])
def like_retrieve_update_destroy_api_view(request, pk):
    # Get the post object
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=404)

    # Check if the user has already liked the post
    try:
        like = Like.objects.get(post=post, user=request.user)
        if request.method == 'DELETE':
            # User has already liked the post, delete the like object
            like.delete()
            # Remove the like object from the post's likes array
           # post.likes.remove(like)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # User has already liked the post, update the like object
            serializer = LikeSerializer(like, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Like.DoesNotExist:
        if request.method == 'POST':
            # User has not liked the post, create a new Like object for the user and post
            like = Like.objects.create(post=post, user=request.user)
            # Update the post's likes array with the new like object
            post.likes.add(like)
            post.save()
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=201)
        else:
            # User has not liked the post, cannot unlike
            return Response({"error": "Cannot unlike. User has not liked the post."}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list_by_author_api_view(request, author):
    user = get_object_or_404(User, username=author)
    posts = Post.objects.filter(author=user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)




@api_view(['GET'])
def posts_with_videos(request):
    posts = Post.objects.exclude(video=None)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile_picture(request):
    pictures = profile_picture.objects.all()
    serializer = profile_pictureSerializer(pictures, many=True)
    return Response(serializer.data)


@api_view(['POST', 'PUT'])
def profile_picture_up(request):
    user = request.user
    try:
        instance = profile_picture.objects.get(user=user)
    except profile_picture.DoesNotExist:
        instance = None

    if request.method == 'POST':
        serializer = profile_pictureSerializer(data=request.data)
        if serializer.is_valid():
            if instance:
                return Response({'message': 'Profile picture already exists. Use PUT method to update.'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not instance:
            return Response({'message': 'Profile picture does not exist. Use POST method to create.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = profile_pictureSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['post'])
def find_similar_users(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', '')
        users = User.objects.all()
        similar_users = []
        for user in users:
            if user.username.lower() == name.lower():
                similar_users.append(user.username)
            elif SequenceMatcher(None, user.username.lower(), name.lower()).ratio() >= 0.5:
                similar_users.append(user.username)
        return JsonResponse({'similar_users': similar_users})
