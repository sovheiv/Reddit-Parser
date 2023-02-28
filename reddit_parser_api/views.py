import json
import time

from django.core.cache import cache
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from .parser import RedditParser
from .utils import url_issue
import logging
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
        return JsonResponse({"success": False, "message": issue}, status=400)
    url = data["url"]

    def do_after():
        logger.info(f"start parsing {url.split('/')[-2]}")
        cache.set(url,"processing")

        parser = RedditParser()
        post_data = parser.get_post_data(url)
        cache.set(url,post_data)
        logger.info(f"parsed {url.split('/')[-2]}")

    resp = ResponseAfter({"success": True}, do_after,status=202)
    resp.set_cookie("url", url)

    return resp


@require_http_methods(["GET"])
def reddit_data(request: HttpRequest):
    data = request.COOKIES

    if issue := url_issue(data, "url", 35, 140, "https://www.reddit.com/r/"):
        return JsonResponse({"success": False, "message": issue},status=400)
    
    url = data["url"]
    if cache.has_key(url):
        logger.info(f"sending data {url.split('/')[-2]}")
        return JsonResponse({"success": True, "post_data": cache.get(url)})
    
    return JsonResponse({"success": False, "post_data":"no data"})
