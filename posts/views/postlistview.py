from django.http import JsonResponse
from django.views.generic import ListView
from django.core.cache import cache

from posts.models import Post


class PostListView(ListView):
    model = Post

    def get(self, request, *args, **kwargs):
        context = cache.get('posts')
        print(cache.get('posts'))

        if context is None:
            posts = Post.objects.all().values('id', 'title', 'content')
            context = {}
            for i in posts:
                context[f'post_{i["id"]}'] = i
            cache.set('posts', context)
        return JsonResponse(context)