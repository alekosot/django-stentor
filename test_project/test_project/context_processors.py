# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stentor.models import Subscriber


def unsubscribe_link(request):
    sub = Subscriber.objects.active().first()
    return {
        'unsubscribing_subscriber': sub,
        'unsubscribe_link': sub.get_unsubscribe_url() if sub else ''
    }
