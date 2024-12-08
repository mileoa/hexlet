from django.urls import path
from hexlet_django_blog.articles import views

urlpatterns = [
    path("", views.index, {"tags": "python", "article_id": 42}, name="article"),
    path("<str:tags>/<int:article_id>/", views.index),
]
