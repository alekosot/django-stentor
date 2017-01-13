# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import checks
from django.utils import six

from stentor import settings as stentor_conf


def _default_mailing_lists_setting_is_valid(**kwargs):
    error = checks.Error(
        'Wrong value for default mailing lists setting.',
        hint=(
            'The STENTOR_DEFAULT_MAILING_LISTS setting must be an iterable of '
            'strings signifying names of MailingLists.'
        ),
        id='stentor.E001'
    )

    try:
        for name in iter(stentor_conf.DEFAULT_MAILING_LISTS):
            if not isinstance(name, six.string_types):
                return [error]
    except TypeError:
        return [error]
    else:
        if isinstance(stentor_conf.DEFAULT_MAILING_LISTS, six.string_types):
            return [error]
    return []


def _default_mailing_lists_exist(**kwargs):
    mailing_lists = kwargs.pop('mailing_lists')
    if mailing_lists.count() != len(stentor_conf.DEFAULT_MAILING_LISTS):
        return [
            checks.Warning(
                'Default MailingLists do not exist',
                hint=(
                    "The STENTOR_DEFAULT_MAILING_LISTS setting should "
                    "correspond to actual MailingList instances. "
                    "Create them or correct the setting's value."
                ),
                id='stentor.W001'
            )
        ]
    return []
