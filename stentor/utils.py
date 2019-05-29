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


# TODO: Add tests
# TODO: Document the change in the function signature
def subscribe(subscriber, to=None, to_default=True):
    """
    Subscribe the subscriber given.

    `subscriber` may be either a `Subscriber` instance or the email to
    subscribe. If a `Subscriber` with this email exists already, it's used
    instead.

    `to` is checked to be (in this order) a `MailingList` name, pk, instance or
    queryset, or failing those, an iterable of `MailingList` names, primary
    keys or instances. If names or pks are given, the corresponding
    `MailingList`s should exist already.

    If `to_default` is `True`, a subscription to the "default" `MailingList`
    will take place as well.

    **WARNING**: Depending on the parameters, this may result in the
    `Subscriber` not having been subscribed to *any* `MailingList`s. This may
    be a desired behavior, so it's tolerated.
    """
    from .models import Subscriber, MailingList

    if type(subscriber) != Subscriber:
        subscriber, created = Subscriber.objects \
            .get_or_create(email=subscriber)

    # Mark the subscriber as active:
    # - if it's a new subscriber and no subscription confirmation is needed
    # - if it's an existing subscriber and not already active
    if (created and not stentor_conf.SUBSCRIPTION_CONFIRMATION)  \
            or (not created and not subscriber.is_active):
        subscriber.is_active = True
        subscriber.save()

    mailing_lists = MailingList.objects.none()  # initial qs to merge others to
    MailingListQuerySet = type(mailing_lists)

    if to:
        if type(to) == str:
            # Assume it's a MailingList's title
            mailing_lists |= MailingList.objects.filter(name=to)
        elif type(to) == int:
            # Assume it's a MailingList's pk
            mailing_lists |= MailingList.objects.filter(pk=to)
        elif isinstance(to, MailingList):
            # TODO: This is simple, but a bit inefficient
            mailing_lists |= MailingList.objects.filter(pk=to.pk)
        elif issubclass(to, type(MailingListQuerySet)):
            mailing_lists |= to
        else:
            # Assume it's an iterable of...
            if all([type(i) == str for i in to]):
                # ... MailingList names
                mailing_lists |= MailingList.objects.filter(name__in=to)
            elif all([type(i) == int for i in to]):
                # ... MailingList pks
                mailing_lists |= MailingList.objects.filter(pk__in=to)
            elif all([isinstance(i, MailingList) for i in to]):
                # ... MailingList instances
                mailing_lists |= MailingList.objects  \
                    .filter(pk__in=[mailing_list.pk for mailing_list in to])
            else:
                raise TypeError(
                    '"to" must be a MailingList name, pk, instance, queryset '
                    'or an iterable of MailingList names, pks or instances.')

    if to_default:
        mailing_lists |= MailingList.objects.default()

    subscriber.mailing_lists.add(*mailing_lists)

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
