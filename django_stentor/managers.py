# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain

from django.core import mail
from django.db import models
from django.utils import timezone

from . import settings as stentor_conf


class MailingListManager(models.Manager):
    def default(self):
        qs = self.get_queryset()
        return qs.get(name=stentor_conf.DEFAULT_MAILING_LIST)


class SubscriberQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(is_active=False)


class SubscriberManager(models.Manager):
    def get_queryset(self):
        return SubscriberQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class ScheduledSendingQuerySet(models.QuerySet):
    def send(self):
        messages = []
        for scheduled_sending in self:
            messages.append(scheduled_sending.get_email_message())

        connection = mail.get_connection()
        connection.send_messages(messages)

    def send_and_delete(self):
        self.send()
        return self.delete()

    def sendable(self):
        now = timezone.now()
        return self.filter(sending_date__lte=now).order_by('sending_date')

    # The implementation below is slow apparently
    # def send_mass_mail(self, **kwargs):
    #     mails = []
    #     for scheduled_sending in self:
    #         mails.append(scheduled_sending.get_data_for_mass_mail())
    #     mail.send_mass_mail(mails, **kwargs)


class ScheduledSendingManager(models.Manager):

    def get_queryset(self):
        return ScheduledSendingQuerySet(self.model, using=self._db)

    def sendable(self):
        return self.get_queryset().sendable()

    def bulk_create_for(
            self, newsletter, mailing_lists=None, subscribers=None, when=None):
        """
        """
        from stentor.models import Subscriber
        if not mailing_lists:
            mailing_lists = newsletter.mailing_lists.all()
        if not subscribers:
            subscribers = newsletter.subscribers.all()
        if not when:
            when = timezone.now()

        mlist_subscribers = Subscriber.objects.filter(
            mailing_lists__in=mailing_lists
        )

        # We join the two iterables into one and we discard duplicates by
        # making the iterable a set.
        unique_subscriber_list = set(chain(mlist_subscribers, subscribers))

        sendings = []

        for subscriber in unique_subscriber_list:
            sendings.append(
                self.model(
                    subscriber=subscriber,
                    newsletter=newsletter,
                    sending_date=when
                )
            )

        self.bulk_create(sendings)
