# -*- coding: utf-8 -*-
import twitter
from config.models import TwitterConfiguration


def get_tweets():
    """
    returns twitter feed with settings as described below, contains all related twitter settings
    """
    twitter_conf = TwitterConfiguration.objects.get()
    api = twitter.Api(twitter_conf)

    return api.GetUserTimeline(
        screen_name='twitter_screen_name',
        exclude_replies=True,
        include_rts=False)  # includes entities