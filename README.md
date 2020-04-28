# iwantdrfmaster
Until the day you become a DRF master ...

# View

# APIView

class PostListAPIView(APIView):
  
List를 보거나(GET), 생성하는(POST) API View 

[!] api/post/

    def get(self, request):
        serializer = PostListSerializer(Post.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = PostListSerializer(data=request.data)
        if serializer.is_valid():  # serializer 검증 (request.data에 대해서)
            serializer.save()  # 검증이 완료되었다면 DB에 생성한다.
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


포스트 내용 수정 삭제 

[!] api/post/<int:pk>/

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

# ViewSet
