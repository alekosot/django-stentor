# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import six

from stentor import settings as stentor_conf


class BaseObfuscationBackend(object):
    """
    Base object for describing the API for obfuscating publicly visible values.

    This is used for:
    - in unsubscription URLs for a specific Subscriber
    - in unsubscription URLs for a Subscriber-Newsletter pair
    - in web view URLs of Newsletters
    - tracker image URLs that are used for tracking email views
    """

    def __init__(self):
        settings = self.validate_settings()
        for key, value in six.iteritems(settings):
            setattr(self, key, value)

    def validate_settings(self):
        """
        Subclasses should make their own checks on their configuration and
        raise an ``ImproperlyConfigured`` exception if they are invalid.
        """
        return stentor_conf.OBFUSCATION_SETTINGS

    # Encoders

    def encode_single_value(self, int):
        raise NotImplementedError('Subclasses must implement this')

    def encode_multiple_values(self, *args):
        raise NotImplementedError('Subclasses must implement this')

    def encode_unsubscribe_hash(self, subscriber):
        """
        This must take into account the creation date of the Subscriber.
        """
        raise NotImplementedError('Subclasses must implement this')

    def encode_email_tracker_hash(self, sending):
        return self.encode_multiple_values(
            sending.newsletter.pk,
            sending.subscriber.pk
        )

    def encode_web_view_hash(self, sending):
        return self.encode_multiple_values(
            sending.newsletter.pk,
            sending.subscriber.pk
        )

    def encode_generic_identifier_hash(
            self, sending=None, newsletter=None, subscriber=None):
        if not sending:
            if not newsletter and not subscriber:
                raise ValueError(
                    'You must provide either a ScheduledSending instance or '
                    'both a Newsletter instance and a Subscriber instance '
                    'as arguments')
            newsletter_pk = newsletter.pk
            subscriber_pk = subscriber.pk
        else:
            newsletter_pk = sending.newsletter.pk
            subscriber_pk = sending.subscriber.pk

        return self.encode_multiple_values(newsletter_pk, subscriber_pk)

    # Decoders

    def decode_single_value_hash(self, hash_string):
        """
        Return a single integer from the hash.
        """
        raise NotImplementedError('Subclasses must implement this')

    def decode_multiple_value_hash(self, hash_string):
        """
        Return all the integers represented by the hash.
        """
        raise NotImplementedError('Subclasses must implement this')

    def decode_unsubscribe_hash(self, hash_string):
        """
        Return the creation date of the Subsriber (as an ordinal) and
        the pk of a Subscriber instance.
        """
        raise NotImplementedError('Subclasses must implement this')

    def decode_email_tracker_hash(self, hash_string):
        """
        Return the pk of a Subscriber instance and the pk of a
        Newsletter instance (in this order).
        """
        return self.decode_multiple_value_hash(hash_string)

    def decode_web_view_hash(self, hash_string):
        """
        Return the pk of a Subscriber instance and the pk of a
        Newsletter instance (in this order).
        """
        return self.decode_multiple_value_hash(hash_string)

    def decode_generic_identifier_hash(self, hash_string):
        """
        Return the pk of a Subscriber instance and the pk of a
        Newsletter instance (in this order).
        """
        return self.decode_multiple_value_hash(hash_string)
