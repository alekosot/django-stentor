# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


# NOTE: These will be implemented in the future
# ALLOW_ANONYMOUS_IDENTIFIER_FOR_WEB_VIEWS = True
#
# # Set this to an empty string if you want to disable public
# ANONYMOUS_IDENTIFIER_FOR_WEB_VIEWS = '_public'

DEFAULT_MAILING_LIST = getattr(
    settings,
    'STENTOR_DEFAULT_MAILING_LIST',
    'default'
)

# TODO: This is essential and we want an error to be raised if it hasn't been
# set. Throw an Exception if it is not set though, giving an easy solution to
# overcome this.
# TODO: Document the arguments passed to this callable.
HASH_GENERATOR = settings.STENTOR_HASH_GENERATOR

# TODO: Add logging
# LOGGING = getattr(
#     settings,
#     'STENTOR_LOGGING',
#     'default'
# )

# If set to None, no slugify will take place. If set to False,
# django.utils.text.slugify will be used with the newsletter subject as input
# and allow_unicode set to False. If set to True, the callable will be passed
# the Newsletter instance, so account for it.
NEWSLETTER_SLUGIFY = getattr(
    settings,
    'STENTOR_NEWSLETTER_SLUGIFY',
    False
)


# NOTE: This is currently useless, but if base/example templates are given this
# could make the templates easily reusable.
# TODO: This is essential and we want an error to be raised if it hasn't been
# set. Make it more clever however, with checking for django.contrib.sites app
# and fetching the url from there.
# PUBLIC_HTTP_HOST = settings.STENTOR_PUBLIC_HTTP_HOST

# This is used in cases where the "admin site" where the creation of
# newsletter takes place is different than the "public site" where email views
# of newsletter take place.
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

# TODO: What's the use case scenario for this? Remove if useless
# SUBSCRIPTION_BACKEND = getattr(
#     settings,
#     'STENTOR_SUBSCRIPTION_BACKEND',
#     'newsletter.backends.filebased.SubscriptionBackend'
# )

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
