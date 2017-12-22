# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain

from django.core import mail
from django.db import models
from django.utils import timezone, six

from . import settings as stentor_conf
from . import checks as stentor_checks


class MailingListManager(models.Manager):
    def check(self, **kwargs):
        errors = super(MailingListManager, self).check(**kwargs)
        default_mailing_lists = self.default()

        errors.extend(
            stentor_checks._default_mailing_lists_setting_is_valid(**kwargs)
        )
        errors.extend(
            stentor_checks._default_mailing_lists_exist(
                mailing_lists=default_mailing_lists, **kwargs
            )
        )

        return errors

    def default(self):
        qs = self.get_queryset()
        return qs.filter(name__in=stentor_conf.DEFAULT_MAILING_LISTS)


class SubscriberQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(is_active=False)

    def recipients_remaining_for(self, newsletter):
        return self.exclude(pk__in=newsletter.past_recipients)


class SubscriberManager(models.Manager):
    def get_queryset(self):
        return SubscriberQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def recipients_remaining_for(self, newsletter):
        return self.get_queryset().recipients_remaining_for(newsletter)


class ScheduledSendingQuerySet(models.QuerySet):
    def send(self):
        from stentor.models import Newsletter

        messages = []
        newsletter_map = {}

        for scheduled_sending in self:
            newsletter_slug = scheduled_sending.newsletter.slug
            subscriber_pk = scheduled_sending.subscriber.pk
            if newsletter_slug not in newsletter_map:
                newsletter_map[newsletter_slug] = []
            newsletter_map[newsletter_slug].append(subscriber_pk)

            messages.append(scheduled_sending.get_email_message())

        connection = mail.get_connection()
        connection.send_messages(messages)

        newsletter_slugs = list(six.iterkeys(newsletter_map))
        newsletters = Newsletter.objects.filter(slug__in=newsletter_slugs)[:]

        # HACK/TODO: This is ugly...
        for newsletter_slug, subscriber_pks in six.iteritems(newsletter_map):
            newsletter = [
                nl for nl in newsletters if nl.slug == newsletter_slug
            ][0]

            newsletter.past_recipients += subscriber_pks
            newsletter.save()

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
            subscribers = newsletter.get_recipients_remaining()
        if not when:
            when = timezone.now()

        mlist_subscribers = Subscriber.objects.filter(
            mailing_lists__in=mailing_lists
        ).recipients_remaining_for(newsletter)

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
