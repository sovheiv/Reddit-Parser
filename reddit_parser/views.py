from django.shortcuts import render
from django.http import JsonResponse, HttpRequest


def index(request: HttpRequest):
    return render(request,"reddit_parser/index.html")
