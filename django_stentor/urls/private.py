# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from stentor.views import private


urlpatterns = [
    url(r'^newsletter$',
        private.NewsletterListView.as_view(),
        name='stentor.newsletter.list'),
    url(r'^newsletter/create$',
        private.NewsletterCreateView.as_view(),
        name='stentor.newsletter.create'),
    url(r'^newsletter/(?P<pk>\d+)/$',
        private.NewsletterUpdateView.as_view(),
        name='stentor.newsletter.update'),
    url(r'^newsletter/(?P<pk>\d+)/delete/$',
        private.NewsletterDeleteView.as_view(),
        name='stentor.newsletter.delete'),

    url(r'^subscriber$',
        private.SubscriberListView.as_view(),
        name='stentor.subscriber.list'),
    url(r'^subscriber/create$',
        private.SubscriberCreateView.as_view(),
        name='stentor.subscriber.create'),
    url(r'^subscriber/(?P<pk>\d+)/$',
        private.SubscriberUpdateView.as_view(),
        name='stentor.subscriber.update'),
    url(r'^subscriber/(?P<pk>\d+)/delete/$',
        private.SubscriberDeleteView.as_view(),
        name='stentor.subscriber.delete'),

    url(r'^mailing_list$',
        private.MailingListListView.as_view(),
        name='stentor.mailing_list.list'),
    url(r'^mailing_list/create$',
        private.MailingListCreateView.as_view(),
        name='stentor.mailing_list.create'),
    url(r'^mailing_list/(?P<pk>\d+)/$',
        private.MailingListUpdateView.as_view(),
        name='stentor.mailing_list.update'),
    url(r'^mailing_list/(?P<pk>\d+)/delete/$',
        private.MailingListDeleteView.as_view(),
        name='stentor.mailing_list.delete'),

    url(r'^scheduled_sending$',
        private.ScheduledSendingListView.as_view(),
        name='stentor.scheduled_sending.list'),
    url(r'^scheduled_sending/create$',
        private.ScheduledSendingCreateView.as_view(),
        name='stentor.scheduled_sending.create'),
    url(r'^scheduled_sending/(?P<pk>\d+)/$',
        private.ScheduledSendingUpdateView.as_view(),
        name='stentor.scheduled_sending.update'),
    url(r'^scheduled_sending/(?P<pk>\d+)/delete/$',
        private.ScheduledSendingDeleteView.as_view(),
        name='stentor.scheduled_sending.delete'),
]
