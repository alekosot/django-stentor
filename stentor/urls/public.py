# *- coding: utf-8 -*-
"""
URL configurations for public views of django-stentor.

NOTE: The subcriber_hash groups in the regular expressions below intentionally
match a lot of strings, so that custom hasher produce compatible results.
"""
from __future__ import unicode_literals

from django.conf.urls import url

from stentor.views import public


app_name = 'stentor'


urlpatterns = [
    url(r'^subscribe/$',
        public.SubscribeView.as_view(),
        name='subscriber.subscribe'),
    url(r'^subscribe/thanks/$',
        public.SubscribeSuccessView.as_view(),
        name='subscriber.subscribe_success'),


    url(r'^unsubscribe/'
            r'(?P<unsubscribe_hash>[^\/\r\n\t\f\v ]+)/'  # NOQA
            r'(?P<newsletter_hash>[^\/\r\n\t\f\v ]+)/$',  # NOQA
        public.UnsubscribeView.as_view(),
        name='subscriber.unsubscribe_from_newsletter'),
    url(r'^unsubscribe/(?P<unsubscribe_hash>[^\/\r\n\t\f\v ]+)/$',
        public.UnsubscribeView.as_view(),
        name='subscriber.unsubscribe'),
    url(r'^unsubscribe/successful$',
        public.UnsubscribeSuccessView.as_view(),
        name='subscriber.unsubscribe_success'),

    url(r'^!/(?P<newsletter_slug>[\w\d_-]+)/image.gif$',
        public.newsletter_email_tracker,
        name='newsletter.email_view_tracker'),

    url(r'^!/'
            r'(?P<newsletter_slug>[\w\d_-]+)/'  # NOQA
            r'(?P<subscriber_hash>[^\/\r\n\t\f\v ]+)/'  # NOQA
            r'image.gif$',  # NOQA
        public.newsletter_email_tracker,
        name='newsletter.email_view_tracker_from_subscriber'),

    url(r'^(?P<newsletter_slug>[\w\d_-]+)/$',
        public.newsletter_web_view_from_anonymous,
        name='newsletter.anonymous_web_view'),

    url(r'^(?P<newsletter_slug>[\w\d_-]+)/'
            r'(?P<subscriber_hash>[^\/\r\n\t\f\v ]+)/$',
        public.newsletter_web_view_from_subscriber,
        name='newsletter.subscriber_web_view'),
]
