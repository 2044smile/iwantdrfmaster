# iwantdrfmaster
Until the day you become a DRF master ...

# Basic
> ## 직렬화 클래스 지정
*  renderer_classes
- default

    - JSON 직렬화 : rest_framework.renders.JSONRenderer
    - HTML 페이지 직렬화 : rest_framework.renderers.TemplateHTMLRenderer
    
> ## 비직렬화 클래스 지정

- parser_classes
- default

    - JSON 포맷 처리 : rest_framework.parsers.JSONParser
    - FormParser : rest_Framework.parsers.FormParser
    
> ## 인증 클래스 지정

- authentication_classes
- default
    - 세션기반 인증 : rest_framework.authentication.SessionAuthentication
    - HTTP basic 인증 : rest_framework.authentication.BasicAuthentication
    
> ## 사용량 제한 클래스 지정

- throttle_classes
- default
    - 빈 튜플
    
> ## 권한 클래스 지정

- permission_classes
- default
    - 누구라도 접근 허용 : rest_framework.permissions.AllowAny
    
> ## 그 외

- 요청에 따라 적절한 직렬화/비직렬화 선택 (JSON, XML . . .)
- 요청 내역에서 API 버전 정보를 탐지할 클래스 지정

# View

# APIView


  
List를 보거나(GET), 생성하는(POST) API View 

[!] api/post/
```python
class PostListAPIView(APIView):
    def get(self, request):
        serializer = PostListSerializer(Post.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = PostListSerializer(data=request.data)
        if serializer.is_valid():  # serializer 검증 (request.data에 대해서)
            serializer.save()  # 검증이 완료되었다면 DB에 생성한다.
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
```

포스트 내용, 수정, 삭제 

[!] api/post/<<int:pk>>/

```python
class PostDetailAPIView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)  # Post.objects.get_or_404(pk=pk) 같은 느낌이다.

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostListSerializer(post, data=request.data)  # 누군가 GET 요청을 보냈을 것이고 request에 데이터가 있을 것
        if serializer.is_valid():  # is_valid 안에 옵션으로 raise_exception=True가 추가될 수 있는데
            # serializer.is_valid(raise_exception=True)
            #  True일 경우 REST framework 가 기본으로 제공하는 exception handler => 400에러를 반환한다.
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostListSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```
# ViewSet

```python
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
```

> Mixin 상속
* APIView는 위에서 봤듯이 각 request method 마다 직접 serializer 처리를 해주었습니다. 하지만 이러한 부분들은 많이 사용되므로 여러 serializer에 대해서 중복이 발생합니다.
따라서 rest_framework.mixins 에서는 이러한 기능들이 미리 구현되어 있습니다.

* CreateModelMixin
* ListModelMixin
* RetrieveModelMixin
* UpdateModelMixin
* DestroyModelMixin

```python
from rest_framework.response import Response
from rest_framework import generics, mixins
from posts.models import Post
from posts.serializers import PostListSerializer


class PostListMixins(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = Post.objects.all()  # 1. queryset은 처음 호출하면 나오는 값을 의미한다. 보통 .all() 을 사용한다.
    serializer_class = PostListSerializer  # 위와 비슷한 의미이지 않을까? 
    
    # 1. 로 설정해두고 Get요청을 보내면 Post의 전체리스트가 Return된다.
    # get_queryset method를 호출하여 아래와 같이 pk가 3인 것을 호출하면 어떻게될까?
    # get_queryset이 위의 queryset을 호출하여 사용한다고 생각하면 될거같다. 3번 째 게시물이 호출된다.

    # https://pjs21s.github.io/queryset/
    # queryset은 서버를 시작할 때 단 한번만 queryset을 생성한다. 혹은 request 발생 시 한번만 queryset 동작한다.
    # 반면에 get_queryset method는 매번 쿼리를 발생시킨다. 즉 get_queryset은 동적으로 사용하고 싶을 때 유용하다.
    def get_queryset(self):
        queryset = Post.objects.filter(pk=3)
        return queryset
    
    # 접속한 유저의 object를 리턴해주고 싶을 때도 사용할 수 있다.     
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request)

```