from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.conf import settings

import logging

logger = logging.getLogger(__name__)


class Status(models.TextChoices):
    PROCESSING = "processing", "PROCESSING"
    PARSED = "parsed", "PARSED"


class Post(models.Model):
    url = models.CharField(max_length=250, help_text="Post url", unique=True)
    content = models.JSONField(null=True)
    likes_num = models.IntegerField(null=True)
    comments_num = models.IntegerField(null=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PROCESSING)
    creation_time = models.DateTimeField(auto_now_add=True)
    parse_time = models.DateTimeField(null=True)

    def is_post(url):
        try:
            post = Post.objects.get(url=url)
        except ObjectDoesNotExist:
            logger.info("no post")
            return False

        if (
            isinstance(post.parse_time, datetime)
            and post.parse_time > datetime.utcnow() + settings.POST_LIFETIME
        ):
            post.delete()
            logger.info("delete old post")
            return False

        logger.info("post exist")
        return post
