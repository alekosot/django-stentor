# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashids

from stentor import settings as stentor_conf
from stentor.obfuscation.base import BaseObfuscationBackend


# TODO: Add a check for this backend so that if there is no 'salt' in settings,
# the user is notified that the obfuscated values will be easily decodable
class HashIdsObfuscationBackend(BaseObfuscationBackend):
    def __init__(self):
        super(HashIdsObfuscationBackend, self).__init__()
        available_settings = ['salt', 'min_length', 'alphabet']
        dikt = {}
        for setting in available_settings:
            conf = getattr(stentor_conf.OBFUSCATION_SETTINGS, setting, None)
            if conf:
                dikt[setting] = conf
        self.hashids = hashids.Hashids(**dikt)

    # Encoders

    def encode_single_value(self, value):
        return self.hashids.encode(value)

    def encode_unsubscribe_hash(self, subscriber):
        ord_day_created = subscriber.creation_date.toordinal()
        return self.hashids.encode(ord_day_created, subscriber.pk)

    def encode_email_tracker_hash(self, sending):
        return self.hashids.encode(
            sending.newsletter.pk, sending.subscriber.pk
        )

    def encode_web_view_hash(self, sending):
        return self.hashids.encode(
            sending.newsletter.pk,
            sending.subscriber_id
        )

    # Decoders

    def decode_single_value_hash(self, hash_string):
        return self.hashids.decode(hash_string)

    def decode_unsubscribe_hash(self, hash_string):
        ord_day_created, subscriber_pk = self.hashids.decode(hash_string)
        return str(ord_day_created), subscriber_pk

    def decode_email_tracker_hash(self, hash_string):
        return self.hashids.decode(hash_string)

    def decode_web_view_hash(self, hash_string):
        return self.hashids.decode(hash_string)


backend = HashIdsObfuscationBackend()
