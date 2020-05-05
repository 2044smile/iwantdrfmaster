from datetime import datetime

from django.http import HttpResponse
from django.views.generic.base import View
from posts.models import Post


def query_test(request):
    posts = Post.objects.create(title='Query Title Test', content='Query Content Test')
    posts.save()
    for i in range(10):
        print(i)

    posts.update_at = datetime.now()
    posts.save()
    return HttpResponse('Oh Yes!!')

class PostBaseListView(View):
    http_method_names = ['get']  # 승인 할 메소드 목록, ex) 'post'만 남겨둔 상태로 GET으로 접속하면 Method Not Allowed 405 Error

    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello I'm django.views.generic.base View!!!")
