from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from hexlet_django_blog.articles.models import Article, ArticleComment
from .forms import ArticleCommentForm, ArticleForm, CommentArticleForm


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


class ArticleView(View):

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=kwargs["id"])
        return render(
            request,
            "articles/show.html",
            context={
                "article": article,
            },
        )


class CommentArticleView(View):

    def get(self, request, *args, **kwargs):
        form = CommentArticleForm()
        return render(request, "comment.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = CommentArticleForm(request.POST)
        if form.is_valid():
            comment = ArticleComment(
                name=form.cleaned_data["content"],
            )
            comment.save()


class ArticleFormCreateView(View):

    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, "articles/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("article")
        return render(request, "articles/create.html", {"form": form})


class ArticleCommentFormView(View):

    def post(self, request, *args, **kwargs):
        form = ArticleCommentForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данных формы на корректность
            form.save()  # Сохраняем форму


class ArticleFormEditView(View):

    def get(self, request, *args, **kwargs):
        article_id = kwargs.get("id")
        article = get_object_or_404(Article, id=article_id)
        form = ArticleForm(instance=article)
        return render(
            request, "articles/edit.html", {"form": form, "article_id": article_id}
        )

    def post(self, request, *args, **kwargs):
        article_id = kwargs.get("id")
        article = Article.objects.get(id=article_id)
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("articles")

        return render(
            request, "articles/update.html", {"form": form, "article_id": article_id}
        )


class ArticleFormDeleteView(View):

    def post(self, request, *args, **kwargs):
        article_id = kwargs.get("id")
        article = Article.objects.get(id=article_id)
        if article:
            article.delete()
        return redirect("articles")
