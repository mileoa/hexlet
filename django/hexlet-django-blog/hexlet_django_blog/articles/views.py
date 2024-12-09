from django.shortcuts import render
from django.http import HttpResponse
from hexlet_django_blog.articles.models import Article
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()[:15]
        return render(
            request,
            "articles/index.html",
            context={
                "articles": articles,
            },
        )
