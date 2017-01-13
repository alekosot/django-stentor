# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


DEFAULT_MAILING_LISTS = getattr(
    settings,
    'STENTOR_DEFAULT_MAILING_LISTS',
    ['default']
)

OBFUSCATION_BACKEND = getattr(
    settings,
    'STENTOR_OBFUSCATION',
    'stentor.obfuscation.dummy.backend'
)

OBFUSCATION_SETTINGS = getattr(
    settings,
    'OBFUSCATION_SETTINGS',
    {}
)

# TODO: Rename to STENTOR_SLUGIFY
# If set to None, no slugify will take place. If set to False,
# django.utils.text.slugify will be used with the newsletter subject as input
# and allow_unicode set to False. If set to True, the callable will be passed
# the Newsletter instance, so account for it.
SLUGIFY = getattr(
    settings,
    'STENTOR_SLUGIFY',
    False
)

# This is used in cases where the "admin/cms site" where the creation of
# newsletters takes place is different than the "public site" where email views
# of newsletters take place.
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
    'stentor.forms.SubscribeForm'  # TODO
)

TEMPLATES = getattr(
    settings,
    'STENTOR_TEMPLATES',
    {
        'default': (
            'newsletter_email.html',  # The first one is for email renders
            'newsletter_web.html'  # The second one for web browser renders
        )
    }
)

UNSUBSCRIBE_FORM = getattr(
    settings,
    'STENTOR_UNSUBSCRIBE_FORM',
    'stentor.forms.UnsubscribeForm'  # TODO
)
