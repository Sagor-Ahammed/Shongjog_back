from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('posts/', post_list_create_api_view, name='post-list'),
    path('posts/<int:pk>/', post_detail_api_view, name='post-detail'),
    path('posts/<str:author>/', post_list_by_author_api_view, name='post_list_by_author_api'),
    path('comments/', comment_list_create_api_view, name='comment-list'),
    path('comments/<int:pk>/', comment_detail_api_view, name='comment-detail'),
    path('likes/', like_list_create_api_view, name='like-list'),
    path('likes/<int:pk>/', like_retrieve_update_destroy_api_view, name='like-detail'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('users/', user_list, name='user-list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
