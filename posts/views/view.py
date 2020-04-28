from django.http import HttpResponse
from django.views.generic.base import View


class PostBaseListView(View):
    http_method_names = ['get']  # 승인 할 메소드 목록, ex) 'post'만 남겨둔 상태로 GET으로 접속하면 Method Not Allowed 405 Error

    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello I'm django.views.generic.base View!!!")
