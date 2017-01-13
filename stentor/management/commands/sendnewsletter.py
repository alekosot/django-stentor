# -*- coding: utf-8 -*-
# TODO: Check docstrings, add tests and add argument for custom batch size
from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError

from stentor import settings as stentor_conf
from stentor.models import ScheduledSending


class Command(BaseCommand):
    """
    Fetches a number of Schedule instances from the database and sends the
    Newsletter to the Subscriber, both as they are defined in the Schedule
    instance. The number of Schedule instances fetched is the first argument
    (a number) or else the defaulf is used, which is 250.

    Examples:
        ``$ python manage.py newsletter_send 500``
        ``$ python manage.py newsletter_send 60 --verbosity=1``

    Options:
        --verbosity=[0]
            Either 0 or any positive number. Default is zero. Any positive
            number displays whether or not emails were successfully sent.
    """
    def handle(self, *args, **options):
        limit = stentor_conf.SCHEDULED_SENDING_BATCH_SIZE

        schedules = ScheduledSending.objects.sendable()

        if limit:  # limit can be 0, which means no limit and thus this check
            # We cannot do ``delete`` on a slice, so...
            untouched_pks = schedules[limit:].values_list('id', flat=True)
            schedules = schedules.exclude(pk__in=untouched_pks)

        schedules.send_and_delete()

    @property
    def help(self):
        return self.__doc__
