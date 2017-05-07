# -*- coding: utf-8 -*-
import logging
import twitter
from config.models import TwitterConfiguration
from twitter import TwitterError


def get_tweets(screen_name='@zedus', count=10, exclude_replies=True, include_rts=False):
    """
    returns twitter feed with settings as described below, contains all related twitter settings
    """
    try:
        twitter_conf = TwitterConfiguration.objects.get()

        api = twitter.Api(**twitter_conf.data)

        return api.GetUserTimeline(
            count=count, exclude_replies=exclude_replies,
            include_rts=include_rts,
        )

    except TwitterError:
        logging.exception("Something happened with twitter api")
