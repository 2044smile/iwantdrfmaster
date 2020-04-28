from rest_framework import viewsets

from posts.models import Post
from posts.serializers.posts import PostListSerializer


class PostViewSet(viewsets.ModelViewSet):  # Django REST framework 브라우저블한 화면이 보여진다.
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    # serializer = PostListSerializer(queryset, many=True) -> ModelSerializer를 상속받았기 때문에 Queryset 변환도 지원
    # serializer.data -> Post의 데이터가 dict 타입으로 출력되고,
    # type(serializer.data) -> <class 'rest_framework.utils.serializer_helpers.ReturnList'>
    # RuturnDict는 순서있는 사전형을 의미하는 OrderedDict를 상속받았다.

    # 실제로 Return 을 Json으로 주고싶다면
    # from rest_framework import Response
    # response = Response(serializer.data)
    # print(response)
    # <Response status_code=200, "text/html; charset=utf-8">
