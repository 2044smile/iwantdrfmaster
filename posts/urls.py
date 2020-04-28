from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostBaseListView
from posts.views.api_view import *
from posts.views.viewset import PostViewSet

# ViewSet의 경우 Router를 이용하여 URL을 등록한다.

router = DefaultRouter()
router.register(r'posts', PostViewSet)  # api/posts

urlpatterns = [
    # Base View
    path('posts_list/', PostBaseListView.as_view(), name='post_list'),

    # ViewSet
    path('', include(router.urls)),

    # FBV API View
    path('post/', PostListAPIView.as_view()),
    path('post/<int:pk>/', PostDetailAPIView.as_view())
]
