# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from stentor import utils as stentor_utils

from .models import Subscriber


class SubscribeForm(forms.Form):
    """
    A form for subscribing to the newsletter to be used in the frontend as a
    simple public form.
    """

    def save(self):
        email = self.cleaned_data['email']
        subscriber = Subscriber.objects.get_or_create(email=email)[0]
        subscriber.is_unsubscribed = True
        return subscriber.save()


class UnsubscribeForm(forms.Form):
    """
    A form for unsubscribing from the newsletter.

    Keep in mind that the ``unsubscribe_hash`` field is important for
    validation. Regular users should not mess with it and both its hidden
    widget and misleading label are on purpose.
    """
    unsubscribe_hash = forms.CharField(
        widget=forms.HiddenInput(), label='name'
    )
    email = forms.EmailField(label="Your email")

    class Meta:
        fields = ('unsubscribe_hash', 'email')

    def clean(self):
        cleaned_data = self.cleaned_data
        unsubscribe_hash = cleaned_data['unsubscribe_hash']

        _request_day, subscribed_day, pk = stentor_utils.hasher.decode(
            unsubscribe_hash
        )

        now = datetime.now()
        request_day = datetime.fromordinal(_request_day)
        if (now - request_day).days > 3:
            raise forms.ValidationError(_(
                'It has been more than 3 days since the unsubscribe request '
                'was made. Please make a new request.'
            ))

        subscribed_day = timezone.fromordinal(subscribed_day)
        try:
            subscriber = Subscriber.objects.get(pk=pk)
        except Subscriber.DoesNotExist:
            raise forms.ValidationError(_(
                'There is no subscription with this email address.'
            ))

        if subscriber.creation_date.day != subscribed_day \
                or subscriber.get_email() != cleaned_data['email']:
            raise forms.ValidationError(_(
                'The web address you used to reach this form is incorrect. '
                'Please check that you have copied it correctly.'
            ))

        self.subscriber = subscriber

        return cleaned_data

    def save(self):
        # ``self.subscriber`` has been assigned in ``self.clean()``
        return self.subscriber.unsubscribe()
