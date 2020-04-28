from django.contrib import admin
from django.urls import path

from posts.views import PostBaseListView

urlpatterns = [
    path('posts_list/', PostBaseListView.as_view(), name='post_list')
]
