from django.urls import path
from .views import (
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
    LikeListCreateAPIView,
    LikeRetrieveUpdateDestroyAPIView
)

app_name = 'api'

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    path('likes/', LikeListCreateAPIView.as_view(), name='like-list'),
    path('likes/<int:pk>/', LikeRetrieveUpdateDestroyAPIView.as_view(), name='like-detail'),
]
