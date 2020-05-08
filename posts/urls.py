from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostBaseListView, query_test
from posts.views.api_view import *
from posts.views.mixins import PostListMixins
from posts.views.postlistview import PostListView
from posts.views.viewset import PostViewSet

router = DefaultRouter()
router.register(r'post_viewset', PostViewSet)

urlpatterns = [
    # Base View
    path('posts_list/', PostBaseListView.as_view(), name='post_list'),
    path('query_test/', query_test, name='query_test'),

    # FBV API View
    path('post/', PostListAPIView.as_view()),
    path('post/<int:pk>/', PostDetailAPIView.as_view()),

    # Custom View Mixins
    path('posts/', PostListMixins.as_view()),

    # ViewSet
    path('', include(router.urls)),
    path('test/', include('posts.view_func_test.view_func_test_urls')),

    # ListView
    path('postlistview/', PostListView.as_view())
]
