from rest_framework import generics
from rest_framework.response import Response

from posts.models import Post
from posts.serializers import PostListSerializer


class PostListGenericAPiView(generics.ListCreateAPIView):  # Create, List
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        print('queryset', queryset)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)



class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):  # Update, Delete
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
