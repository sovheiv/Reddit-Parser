from django.urls import path, include

urlpatterns = [
    path("api/", include("reddit_parser_api.urls")),
]
