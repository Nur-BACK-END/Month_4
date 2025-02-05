from django.shortcuts import render, HttpResponse
import random


def text_view(request):
    return HttpResponse(f"Hello World{random.randint (1,100)}")


def html_view(request):
    return render(request, "main.html")

