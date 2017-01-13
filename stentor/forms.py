# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from stentor.utils import obfuscator, subscribe

from .models import Subscriber


class SubscribeForm(forms.Form):
    """
    A form for subscribing to the newsletter to be used in the frontend as a
    simple public form.
    """
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data['email']
        subscriber = subscribe(email)
        return subscriber


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
        cleaned_data = super(UnsubscribeForm, self).clean()

        # Skip this, if the email field did not survive previous validation
        if 'email' not in cleaned_data:
            return cleaned_data

        unsubscribe_hash = cleaned_data['unsubscribe_hash']

        __, subscriber_pk = obfuscator.decode_unsubscribe_hash(
            unsubscribe_hash
        )

        try:
            subscriber = Subscriber.objects.get(pk=subscriber_pk)
        except Subscriber.DoesNotExist:
            raise forms.ValidationError(_(
                'There is no subscriber with this email address registered.'
            ))

        if subscriber.get_email() != cleaned_data['email']:
            raise forms.ValidationError(_(
                'The web address you used to reach this form is incorrect. '
                'Please check that you have copied it correctly.'
            ))

        self.subscriber = subscriber

        return cleaned_data

    def save(self):
        # ``self.subscriber`` has been assigned in ``self.clean()``
        return self.subscriber.unsubscribe()
