from django.shortcuts import render
from .models import Post


def blog_list(request):
    blogs=Post.objects.all() #Post 모델이 있을 때, DB에서 가져오기
    context={'blogs':blogs}
    return render(request, "blog/blog_list.html", context)


def blog_details(request, pk):
    blog = Post.objects.get(pk=pk)
    context = {'blog':blog}
    return render(request, "blog/blog_details.html", context)
