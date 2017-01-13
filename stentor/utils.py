# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import settings as stentor_conf
from django.utils.module_loading import import_string


obfuscator = import_string(stentor_conf.OBFUSCATION_BACKEND)


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
