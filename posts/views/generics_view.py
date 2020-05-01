from rest_framework import generics
from posts.models import Post
from posts.serializers import PostListSerializer


class PostListGenericAPiView(generics.ListCreateAPIView):  # Create, List
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):  # Update, Delete
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
