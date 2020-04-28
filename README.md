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


JSON 직렬화 : rest_framework.renderers.JSONRenderer
HTML 페이지 직렬화 : rest_framework.renderers.TemplateHTMLRenderer
비직렬화 클래스 지정

parser_classes

default

JSON 포맷 처리 : rest_framework.parsers.JSONParser
FormParser : rest_framework.parsers.FormParser
MultiPartParser : rest_framework.parsers.MultiPartParser
인증 클래스 지정

authentication_classes

default

세션기반인증 : rest_framework.authentication.SessionAuthentication
HTTP basic 인증 : rest_framework.authentication.BasicAuthentication
사용량 제한 클래스 지정

throttle_classes

default

빈 튜플
권한 클래스 지정

permission_classes

default

누구라도 접근 허용 : rest_framework.permissions.AllowAny
요청에 따라 적절한 직렬화/비직렬화 선택

content_negotiation_class

같은 URL 요청에 대해서 JSON 응답을 할 지, HTML 응답을 할 지 판단

default

rest_framework.negotiation.DefaultContentNegotiation
요청 내역에서 API 버전 정보를 탐지할 클래스 지정

versioning_class

요청 URL의 HEADER에서 버전 정보를 탐지하여 맞는 버전을 호출

default

버전 정보를 탐지하지 않습니다. : None

# View

# APIView


  
List를 보거나(GET), 생성하는(POST) API View 

[!] api/post/
```
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

```
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
