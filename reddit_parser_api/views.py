import json
import logging

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Post, Status
from .parser import RedditParser
from .utils import url_issue
from datetime import datetime


logger = logging.getLogger(__name__)


class ResponseAfter(JsonResponse):
    def __init__(self, data, do_after, **kwargs):
        super().__init__(data, **kwargs)
        self.do_after = do_after

    def close(self):
        super().close()
        self.do_after()


@require_http_methods(["POST"])
def parse_reddit(request: HttpRequest):
    data = json.loads(request.body.decode())

    if issue := url_issue(data, "url", 35, 140, "https://www.reddit.com/r/"):
        return JsonResponse({"success": False, "message": f"{issue} in request body"}, status=400)
    url = data["url"]

    def do_after():
        post_name = url.split("/")[-2]

        if Post.is_post(url):
            logger.info(f"{post_name} is already parsed")
            return True

        logger.info(f"start parsing {post_name}")
        post = Post(url=url)
        parser = RedditParser()
        post_data = parser.get_post_data(url)

        post.content = post_data["content"]
        post.comments_num = post_data["comments_num"]
        post.likes_num = post_data["likes_num"]

        post.parse_time = datetime.utcnow()
        post.status = Status.PARSED

        post.save()

        logger.info(f"parsed {post_name}")

    resp = ResponseAfter({"success": True}, do_after, status=202)
    resp.set_cookie("url", url)

    return resp


@require_http_methods(["GET"])
def reddit_data(request: HttpRequest):
    data = request.COOKIES

    if issue := url_issue(data, "url", 35, 140, "https://www.reddit.com/r/"):
        return JsonResponse({"success": False, "message": f"{issue} in cookies"}, status=400)

    url = data["url"]

    if post := Post.is_post(url):
        logger.info(f"sending data {url.split('/')[-2]}")
        post_data = {
            "url": url,
            "content": post.content,
            "likes_num": post.likes_num,
            "comments_num": post.comments_num,
        }
        return JsonResponse({"success": True, "post_data": post_data})

    return JsonResponse({"success": False, "post_data": "no data"})
