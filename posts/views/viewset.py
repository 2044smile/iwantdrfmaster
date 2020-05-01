from posts.models import Post
from posts.serializers import PostListSerializer
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):  # create, list, update, delete
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
