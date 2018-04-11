# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.admin import widgets
from django.utils.translation import ugettext_lazy as _

from stentor.utils import obfuscator, subscribe

from .models import Subscriber, Newsletter


class ScheduleNewsletterForm(forms.Form):
    """
    A form for scheduling the chosen newsletters for sendind, used in an
    intedmediate action in newsletter's admin page.
    """
    slug = forms.CharField(required=False, widget=forms.HiddenInput)
    subject = forms.CharField(required=False, widget=forms.HiddenInput)
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    chosen_date = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())


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

    The ``newsletter_hash`` field is used in the case where the unsubscribe
    URL was followed from within the content of a Newsletter.
    """
    unsubscribe_hash = forms.CharField(
        widget=forms.HiddenInput(), label='Name'
    )
    newsletter_hash = forms.CharField(
        widget=forms.HiddenInput(), label='Last name', required=False
    )
    email = forms.EmailField(label="Your email")

    class Meta:
        fields = ('unsubscribe_hash', 'email')

    def clean(self):
        self.newsletter = None

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

        newsletter_hash = self.cleaned_data.get('newsletter_hash')

        if newsletter_hash:
            pk = obfuscator.decode_single_value_hash(newsletter_hash)[0]
            try:
                newsletter = Newsletter.objects.get(pk=pk)
            except Newsletter.DoesNotExist:
                # NOTE: For this to happen, it is certain that the user is
                # messing with the hidden fields of the form (ie is a
                # "malicious" user. Remember that that the hash has been
                # validated in the view that built this form's initial data)
                raise ValidationError(_(
                    'Please simply enter your email address'
                ))
            else:
                self.newsletter = newsletter

        self.subscriber = subscriber

        return cleaned_data

    def save(self):
        if self.newsletter:
            self.newsletter.unsubscribe_recipient(self.subscriber)
        else:
            # ``self.subscriber`` has been assigned in ``self.clean()``
            self.subscriber.unsubscribe()
