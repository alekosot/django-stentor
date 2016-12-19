# *- coding: utf-8 -*-
"""
URL configurations for public views of django-stentor.

NOTE: The subcriber_hash groups in the regular expressions below intentionally
match a lot of strings, so that custom hasher produce compatible results.
"""
from __future__ import unicode_literals

from django.conf.urls import url

from stentor.views import public


urlpatterns = [
    url(r'^subscribe/$',
        public.SubscribeView.as_view(),
        name='stentor.subscriber.subscribe'),
    url(r'^subscribe/thanks/$',
        public.SubscribeSuccessView.as_view(),
        name='stentor.subscriber.subscribe_success'),

    url(r'^unsubscribe/(?P<unsubscribe_hash>[\S^/]+)/$',
        public.UnsubscribeView.as_view(),
        name='stentor.subscriber.unsubscribe'),
    url(r'^unsubscribe/successful$',
        public.UnsubscribeSuccessView.as_view(),
        name='stentor.subscriber.unsubscribe_success'),

    url(r'^!/(?P<newsletter_slug>[\w\d_-]+)/image.gif$',
        public.newsletter_email_tracker,
        name='stentor.newsletter.email_view_tracker'),

    url(r'^!/(?P<newsletter_slug>[\w\d_-]+)/(?P<subscriber_hash>[\S^/]+)/image.gif$',  # NOQA
        public.newsletter_email_tracker,
        name='stentor.newsletter.email_view_tracker'),

    url(r'^(?P<newsletter_slug>[\w\d_-]+)/$',
        public.newsletter_web_view_from_anonymous,
        name='stentor.newsletter.anonymous_web_view'),

    url(r'^(?P<newsletter_slug>[\w\d_-]+)/(?P<subscriber_hash>[\S^/]+)/$',
        public.newsletter_web_view_from_subscriber,
        name='stentor.newsletter.subscriber_web_view'),
]
