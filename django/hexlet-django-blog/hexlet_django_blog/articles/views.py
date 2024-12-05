from django.shortcuts import render
from django.http import HttpResponse
from hexlet_django_blog.articles.apps import ArticleConfig


def index(request):
    return render(request, "articles/index.html", context={"name": ArticleConfig.name})
