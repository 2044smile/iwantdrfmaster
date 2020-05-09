# iwantdrfmaster
Until the day you become a DRF master ...

그 외 테스트하고 싶은 것을 테스트하는 레포입니다.
* Django-redis-cache
* Git Action Django

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
# Custom View

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
    
    def get(self, request, *args, **kwargs):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request)

```

> Generics APIView
* Mixin을 상속함으로서 반복되는 내용을 많이 줄일 수 있었습니다. 하지만 여러 개를 상속해야 하다보니 가독성이 떨어집니다.
다행히도 rest_framework 에서는 저들을 상속한 새로운 클래스를 정의해놨습니다.

* generics.CreateAPIView: 생성
* generics.ListAPIView: 목록
* generics.RetrieveAPIView: 조회
* generics.DestroyAPIView: 삭제
* generics.UpdateAPIView: 수정
* generics.RetrieveUpdateAPIView: 조회/수정
* generics.RetrieveDestroyAPIView: 조회/삭제
* generics.ListCreateAPIView: 목록/생성
* generics.RetrieveUpdateDestroyAPIView: 조회/생성/삭제

```python
from rest_framework import generics
from posts.models import Post
from posts.serializers import PostListSerializer


class PostListGenericAPiView(generics.ListCreateAPIView):  # Create, List
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):  # Update, Delete
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


# generics.ListCreateAPIView의 동작은 아래와 같다.
class POstListGenericAPIView(generics.ListCreateAPIView):)
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def list(self, request):
        queryset = self.get_queryset # 위의 queryset을 가져온다.
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

```

# ViewSet
* 마지막으로 알아볼 ViewSet입니다. generics APIView를 통해서 코드를 많이 간소화 하였지만 아직 queryset과 serializer_class가 공통적인데도 불구하고
따로 기재해주어야 합니다. 이를 한번에 처리해주는게 ViewSet 입니다.
* ViewSet은 CBV가 아닌 헬퍼클래스로 두 가지 종류가 있습니다.
    1. viewsets.ReadOnlyModelViewSet: 목록 조회, 특정 레코드 조회
    2. viewsets.ModelViewSet: 목록 조회, 특정 레코드 생성/조회/수정/삭제
* ViewSet은 url 등록 시 Router로 편리하게 URL을 관리할 수 있습니다.
* 아래코드를 보면 별 기능이 없어보여도 해당 엔드포인트로 CRUD를 사용할 수 있습니다.
```python
from posts.models import Post
from posts.serializers import PostListSerializer
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):  # create, list, update, delete
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

```

# Test
> perform_create
* perform_create 메소드를 알아보기 전에 create가 어떻게 동작하는지 알아보겠습니다.
```python
# viewsets.py
def create(self, request, *args, **kwargs):
    super().create(request, *args, **kwargs)

# 위 메서드를 호출하면 아래의 CreateModelMixin을 거치게 됩니다.

class CreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # request의 data attribute를 가져옴
        # request.data에는 HTTP Multi Part Form으로 전송된 POST 필드값과 File들이 저장되어 있습니다.
        serializer.is_valid(raise_exception=True)  # Serializer를 통해 유효성 검사
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
```
* 따라서 이것을 토대로 Create Model Mixin을 변경하면 기본적으로 제공하는 여러 절차들을 수행하면서도 커스텀된 POST 데이터 값을 넣을 수 있습니다.