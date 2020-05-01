from rest_framework.response import Response
from rest_framework import generics, mixins
from posts.models import Post
from posts.serializers import PostListSerializer


class PostListMixins(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request)
