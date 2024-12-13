from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.urls import reverse


class Index(View):

    def get(self, request, *args, **kwargs):
        return redirect(reverse("articles"))


def about(request):
    tags = ["обучение", "программирование", "python", "oop"]
    return render(request, "about.html", context={"tags": tags})
