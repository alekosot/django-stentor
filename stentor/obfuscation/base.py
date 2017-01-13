# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import six

from stentor import settings as stentor_conf


class BaseObfuscationBackend(object):

    def __init__(self):
        self.validate_settings()
        for key, value in six.iteritems(stentor_conf.OBFUSCATION_SETTINGS):
            setattr(self, key, value)

    def validate_settings(self):
        """
        Subclasses should make their own checks on their configuration and
        raise an ``ImproperlyConfigured`` exception if they are invalid.
        """
        pass

    # Encoders

    def encode_unsubscribe_hash(self, subscriber):
        """
        This must take into account the creation date of the Subscriber.
        """
        raise NotImplementedError('Subclasses must implement this')

    def encode_email_tracker_hash(self, sending):
        raise NotImplementedError('Subclasses must implement this')

    def encode_web_view_hash(self, sending):
        raise NotImplementedError('Subclasses must implement this')

    # Decoders

    def decode_unsubscribe_hash(self, hash_string):
        """
        Should return the creation date of the Subsriber (as an ordinal) and
        the pk of a Subscriber instance or raise an ``ObjectDoesNotExist``
        exception.
        """
        raise NotImplementedError('Subclasses must implement this')

    def decode_email_tracker_hash(self, hash_string):
        """
        Should return the pk of a Subscriber instance and the pk of a
        Newsletter instance (in this order), or raise an ``ObjectDoesNotExist``
        exception.
        """
        raise NotImplementedError('Subclasses must implement this')

    def decode_web_view_hash(self, hash_string):
        """
        Should return the pk of a Subscriber instance and the pk of a
        Newsletter instance (in this order), or raise a
        ``django.core.exceptions.ObjectDoesNotExist`` exception.
        """
        raise NotImplementedError('Subclasses must implement this')
