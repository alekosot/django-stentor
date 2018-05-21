# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.utils.module_loading import import_string

from . import settings as stentor_conf


obfuscator = import_string(stentor_conf.OBFUSCATION_BACKEND)

TEMPLATE_CHOICES = tuple((name, name) for name in stentor_conf.TEMPLATES)


def get_public_site_url(with_protocol=True):
    if not stentor_conf.PUBLIC_SITE_URL:
        except_msg = (
            'You must either set the STENTOR_PUBLIC_SITE_URL setting '
            'or have the django.contrib.sites app installed and set up.'
        )

        try:
            from django.contrib.sites.models import Site
        except RuntimeError:
            raise ImproperlyConfigured(except_msg)
        else:
            try:
                public_site_url = 'https://' if with_protocol else ''
                public_site_url += Site.objects.get_current().domain
            except ImproperlyConfigured:
                except_msg += "It seems you haven't set the SITE_ID setting."
                raise ImproperlyConfigured(except_msg)

    else:
        public_site_url = stentor_conf.PUBLIC_SITE_URL

    return public_site_url


# TODO: Add test
def subscribe(email, add_to_default=True, mailing_lists=None, subscriber=None):
    """
    TODO
    """
    from .models import Subscriber, MailingList

    if not subscriber:
        subscriber, __ = Subscriber.objects.get_or_create(email=email)

    if not subscriber.is_active:
        subscriber.is_active = True
        subscriber.save()

    mailing_list_ids = []

    if add_to_default:
        default_mailing_lists = MailingList.objects.default()
        mailing_list_ids += [mlist.id for mlist in default_mailing_lists]

    if mailing_lists:
        mailing_list_ids += [mlist.id for mlist in mailing_lists]

    subscriber.mailing_lists.add(*mailing_list_ids)

    return subscriber


def subscribe_multiple(emails, add_to_default=True, mailing_lists=None):
    """
    TODO
    """
    from .models import Subscriber

    # Fetch all emails and keep the unique emails that aren't already
    # subscribed so we can create them. Also keep the emails that are
    # already subscribed so we can update their mailing lists.
    imported_emails = set(emails)
    all_emails = set(Subscriber.objects.values_list('email', flat=True))
    new_emails = imported_emails - all_emails
    existing_emails = all_emails & imported_emails

    # Create instances for new subscribers and bulk create them
    now = timezone.now()
    new_subscribers = [
        Subscriber(email=email, creation_date=now, update_date=now)
        for email in new_emails
    ]
    created_subscribers = Subscriber.objects.bulk_create(new_subscribers)

    # NOTE possible race condition?
    # Create subscribers and mailing lists through table instances
    # and bulk insert them to the through model.
    SubscriberThroughModel = Subscriber.mailing_lists.through
    subscriber_through_instances = [
        SubscriberThroughModel(
            subscriber_id=subscriber.id,
            mailinglist_id=mailing_list.id
        )
        for subscriber in created_subscribers
        for mailing_list in mailing_lists
    ]
    SubscriberThroughModel.objects.bulk_create(subscriber_through_instances)

    # Update the mailing lists of existing subscribers
    mailing_list_ids = [mlist.id for mlist in mailing_lists]
    existing_subscribers = Subscriber.objects.filter(email__in=existing_emails)
    for subscriber in existing_subscribers:
        subscriber.mailing_lists.add(*mailing_list_ids)

    return (len(new_subscribers), len(existing_subscribers))
