from django.urls import path

from posts.view_func_test.perform_create import PostPerformCreateTest

urlpatterns = [
    path('perform_create/', PostPerformCreateTest.as_view({'post': 'create'})),
]
