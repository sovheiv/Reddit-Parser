from django.urls import path

from . import views

urlpatterns = [
    path("parse_reddit", views.parse_reddit, name="parse_reddit"),
    path("reddit_data", views.reddit_data, name="reddit_data"),
]
