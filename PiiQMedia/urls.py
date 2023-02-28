from django.urls import path, include

urlpatterns = [
    path("api/", include("reddit_parser_api.urls")),
    path("", include("reddit_parser.urls")),
]
