# -*- coding: utf-8 -*-
import logging
import twitter
from config.models import TwitterConfiguration


def get_tweets():
    """
    returns twitter feed with settings as described below, contains all related twitter settings
    """
    try:
        twitter_conf = TwitterConfiguration.objects.get()

        api = twitter.Api(**twitter_conf.data)

        return api.GetUserTimeline(
            screen_name='twitter_screen_name',
            exclude_replies=True,
            include_rts=False)  # includes entities
    except Exception:
        logging.exception("Something with twitter api happened")
        return {}