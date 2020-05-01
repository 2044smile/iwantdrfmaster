from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostBaseListView
from posts.views.api_view import *
from posts.views.viewset import PostListMixins

# ViewSet의 경우 Router를 이용하여 URL을 등록한다.

urlpatterns = [
    # Base View
    path('posts_list/', PostBaseListView.as_view(), name='post_list'),

    # FBV API View
    path('post/', PostListAPIView.as_view()),
    path('post/<int:pk>/', PostDetailAPIView.as_view()),

    # Custom View Mixins
    path('posts/', PostListMixins.as_view())
]
