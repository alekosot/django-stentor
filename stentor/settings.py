# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


# A list of callables that modify the context of a Newsletter's renders. These
# handlers take a dictionary as the first argument (the "base" context of the
# render) and a string argument that signifies the nature of the render
# ('email_html' and 'web_html' for the moment). They should all return a
# dictionary (empty or not).
CONTEXT_HANDLERS = getattr(
    settings,
    'STENTOR_CONTEXT_HANDLERS',
    ['']
)


DEFAULT_MAILING_LISTS = getattr(
    settings,
    'STENTOR_DEFAULT_MAILING_LISTS',
    ['Website subscribers']
)

OBFUSCATION_BACKEND = getattr(
    settings,
    'STENTOR_OBFUSCATION_BACKEND',
    'stentor.obfuscation.dummy.backend'
)

OBFUSCATION_SETTINGS = getattr(
    settings,
    'STENTOR_OBFUSCATION_SETTINGS',
    {}
)

# If set to None, no slugify will take place. If set to False,
# django.utils.text.slugify will be used with the newsletter subject as input
# and allow_unicode set to False. If set to True, the callable will be passed
# the Newsletter instance, so account for it.
SLUGIFY = getattr(
    settings,
    'STENTOR_SLUGIFY',
    False
)

# The "base" URL that will serve the tracking image of newsletters, their web
# views and the unsubscription of Subscribers.
# NOTE: If this is not set, stentor tries to get the url from the current Site,
# as given by the django.contrib.sites app.
PUBLIC_SITE_URL = getattr(
    settings,
    STENTOR_PUBLIC_SITE_URL,
    ''
)

# This is used in cases where the "admin/cms site", where the creation of
# newsletters takes place, is different than the "public site" where web
# views of newsletters take place.
PUBLIC_URLCONF = getattr(
    settings,
    'STENTOR_PUBLIC_URLCONF',
    settings.ROOT_URLCONF
)

# TODO: Is this used or needed as it is now? Change the default to an empty
# string for disabling it.
REPLY_TO = getattr(
    settings,
    'STENTOR_REPLY_TO',
    (settings.DEFAULT_FROM_EMAIL,)
)

SENDER_EMAIL = getattr(
    settings,
    'STENTOR_SENDER_EMAIL',
    settings.DEFAULT_FROM_EMAIL
)

SENDER_NAME = getattr(
    settings,
    'STENTOR_SENDER_NAME',
    ''
)

SCHEDULED_SENDING_BATCH_SIZE = getattr(
    settings,
    'STENTOR_SCHEDULED_SENDING_BATCH_SIZE',
    250
)

if SENDER_NAME:
    SENDER_VERBOSE = '{} <{}>'.format(SENDER_NAME, SENDER_EMAIL)
else:
    SENDER_VERBOSE = SENDER_EMAIL

SUBSCRIBE_FORM = getattr(
    settings,
    'STENTOR_SUBSCRIBE_FORM',
    'stentor.forms.SubscribeForm'
)

TEMPLATES = getattr(
    settings,
    'STENTOR_TEMPLATES',
    {
        'Custom': (
            'stentor/newsletter/custom_email.html',  # template for email views
            'stentor/newsletter/custom_web.html'  # template for web views
        )
    }
)

UNSUBSCRIBE_FORM = getattr(
    settings,
    'STENTOR_UNSUBSCRIBE_FORM',
    'stentor.forms.UnsubscribeForm'
)
