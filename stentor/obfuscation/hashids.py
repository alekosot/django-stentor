# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashids

from stentor import settings as stentor_conf
from stentor.obfuscation.base import BaseObfuscationBackend


class HashIdsObfuscationBackend(BaseObfuscationBackend):
    def __init__(self):
        super(HashIdsObfuscationBackend, self).__init__()
        available_settings = ['salt', 'min_length', 'alphabet']
        dikt = {}
        for setting in available_settings:
            dikt[setting] = stentor_conf.OBFUSCATION_SETTINGS[setting]
        self.hashids = hashids.Hashids(**dikt)

    # Encoders

    def encode_unsubscribe_hash(self, subscriber):
        ord_day_created = subscriber.creation_date.toordinal()
        return self.hashids.encode(ord_day_created, subscriber.pk)

    def encode_email_tracker_hash(self, sending):
        return self.hashids.encode(sending.subscriber_id)

    def encode_web_view_hash(self, sending):
        return self.hashids.encode(sending.subscriber_id)

    # Decoders

    def decode_unsubscribe_hash(self, hash_string):
        return self.hashids.decode(hash_string)[0]

    def decode_email_tracker_hash(self, hash_string):
        return self.hashids.decode(hash_string)

    def decode_web_view_hash(self, hash_string):
        return self.hashids.decode(hash_string)


backend = HashIdsObfuscationBackend()
