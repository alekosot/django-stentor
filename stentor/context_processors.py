# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.module_loading import import_string

from stentor import settings as stentor_conf


def subscribe_form(request):
    form = import_string(stentor_conf.SUBSCRIBE_FORM)
    return {
        'newsletter_subscribe_form':  form()
    }
