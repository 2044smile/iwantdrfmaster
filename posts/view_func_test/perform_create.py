from rest_framework import mixins, viewsets

from posts.models import Post
from posts.serializers import PostListSerializer


class PostPerformCreateTest(mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def perform_create(self, serializer):
        print('serializer', serializer)
        print(serializer.validated_data)
