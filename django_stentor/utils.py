# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import settings as stentor_conf


hasher = stentor_conf.HASH_GENERATOR  # NOQA


# TODO: Add test
# TODO: Complete this.
def subscribe(self, email, add_to_default=True, mailing_lists=None,
              subscriber=None):
    """
    Creates SubscriberTag instances. Subscriber is selected/created based
    on the email provided and Tag is selected/created based on the current
    language. If extra_tags are provided then **extra** SubscriberTag
    instances are created for the extra tags, which are also
    created/selected.
    """
    from .models import Subscriber, MailingList

    created = False

    if not subscriber:
        subscriber, created = Subscriber.get_or_create(email=email)

    if not subscriber.is_active:
        subscriber.is_active = True
        subscriber.save()

    if add_to_default:
        mailing_lists = MailingList.objects.filter()
        default_mailing_list = MailingList.objects.default()
        mailing_lists = [default_mailing_list]
