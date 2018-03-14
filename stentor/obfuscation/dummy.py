# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stentor.obfuscation.base import BaseObfuscationBackend


class DummyObfuscationBackend(BaseObfuscationBackend):
    """
    A dummy obfuscation backend that does **NO** actual obfuscation.
    """
    # Encoders

    def encode_single_value(self, value):
        return value

    def encode_unsubscribe_hash(self, subscriber):
        ord_day_created = subscriber.creation_date.toordinal()
        return '{}-{}'.format(ord_day_created, subscriber.pk)

    def encode_email_tracker_hash(self, sending):
        return '{}-{}'.format(sending.newsletter.pk, sending.subscriber.pk)

    def encode_web_view_hash(self, sending):
        return '{}-{}'.format(
            sending.newsletter.pk,
            sending.subscriber.pk
        )

    # Decoders

    def decode_single_value_hash(self, hash_string):
        return hash_string

    def decode_unsubscribe_hash(self, hash_string):
        return hash_string.split('-')

    def decode_email_tracker_hash(self, hash_string):
        return hash_string.split('-')

    def decode_web_view_hash(self, hash_string):
        return hash_string.split('-')


backend = DummyObfuscationBackend()
