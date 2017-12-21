# -*- coding: utf-8 -*-
"""
TODO: Docstrings are a bit old.
"""
from __future__ import unicode_literals

from itertools import chain

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.db import models
from django.template import Template, Context
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import ugettext as _

from . import settings as stentor_conf
from . import managers as stentor_managers
from .utils import obfuscator, subscribe as subscribe_util


@python_2_unicode_compatible
class MailingList(models.Model):
    """
    """
    name = models.CharField(max_length=255, unique=True)

    objects = stentor_managers.MailingListManager()

    class Meta:
        default_related_name = 'mailing_lists'
        verbose_name = 'newsletter mailing list'
        verbose_name_plural = 'newsletter mailing lists'

    def __str__(self):
        return self.name

    def get_subscriber_emails(self):
        for subscriber in self.subscribers.all():
            yield subscriber.get_email()


@python_2_unicode_compatible
class Subscriber(models.Model):
    """
    A newsletter subscriber representation with minimal extra information.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    mailing_lists = models.ManyToManyField(MailingList)
    creation_date = models.DateTimeField(blank=True)
    update_date = models.DateTimeField(blank=True)

    objects = stentor_managers.SubscriberManager()

    class Meta:
        default_related_name = 'subscribers'
        verbose_name = 'newsletter subscriber'
        verbose_name_plural = 'newsletter subscribers'

    def __str__(self):
        return self.email

    def clean(self):
        if not self.email and not self.user:
            raise ValidationError(_(
                'You must provide at least an email address or a User.'))

    def save(self, *args, **kwargs):
        self.clean()
        now = timezone.now()
        self.update_date = now
        if not self.creation_date:
            self.creation_date = now
        return super(Subscriber, self).save(*args, **kwargs)

    def get_email(self):
        return self.email or self.user.email

    def subscribe(self, mailing_lists=None):
        return subscribe_util(email=self.email, mailing_lists=mailing_lists)

    def unsubscribe(self, mailing_lists=None):
        self.is_active = False
        self.save()

        if mailing_lists:
            self.unsubscribe_from(mailing_lists)

    # TODO: Check that this works correctly
    def unsubscribe_from(self, mailing_lists=None):
        if not mailing_lists:
            mailing_lists = MailingList.objects.default()
        self.mailing_lists.remove(mailing_lists)

    def get_unsubscribe_url(self):
        """
        Note that the resolution of dates below is only down to day.
        """
        unsubscribe_hash = obfuscator.encode_unsubscribe_hash(self)
        return reverse_lazy(
            'stentor:subscriber.unsubscribe',
            kwargs={'unsubscribe_hash': unsubscribe_hash},
            urlconf=stentor_conf.PUBLIC_URLCONF,
        )


@python_2_unicode_compatible
class Newsletter(models.Model):
    """
    Representation of a newsletter.
    """
    TEMPLATE_CHOICES = tuple((name, name) for name in stentor_conf.TEMPLATES)

    subject = models.CharField(max_length=255)
    mailing_lists = models.ManyToManyField(
        MailingList, blank=True, help_text=_(
            'Select the mailing lists, to the subscribers of which, the '
            'newsletter should be sent to. If a subscriber is in more than '
            'one mailing list, the newsletter will be sent only once to '
            'them.'))
    subscribers = models.ManyToManyField(
        Subscriber, blank=True, related_name='explicitly_assigned_newsletters',
        help_text=_(
            'Additional subscribers where the newsletter should be sent to. '
            'If the selected subscribers are in any selected mailing lists, '
            'the newletter will still be sent only once to them.'))
    slug = models.SlugField(unique=True, max_length=255)

    template = models.CharField(choices=TEMPLATE_CHOICES, max_length=255)

    email_html = models.TextField(help_text=_('This is filled automatically.'))
    web_html = models.TextField(help_text=_('This is filled automatically.'))

    custom_email_html = models.TextField(blank=True, help_text=_(
        'Custom HTML for the newsletter\'s email views. The template selected '
        'should support this, for this to have any effect.'))
    custom_web_html = models.TextField(blank=True, help_text=_(
        'Custom HTML for the newsletter\'s web views. The template selected '
        'should support this, for this to have any effect.'))

    past_recipients = ArrayField(
        models.IntegerField(blank=True, null=True), default=list)
    email_impressions = ArrayField(
        models.IntegerField(blank=True, null=True), default=list)
    web_impressions = ArrayField(
        models.IntegerField(blank=True, null=True), default=list)

    creation_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        default_related_name = 'newsletters'
        verbose_name = 'newsletter'
        verbose_name_plural = 'newsletters'

    def __str__(self):
        return self.subject

    def clean(self):
        if self.pk and not self.mailing_lists.exists() \
                and not self.subscribers.exists():
            raise ValidationError(_(
                'You must provide either at least one mailing list or at '
                'least one subscriber to send this newsletter to.'))

    def save(self, *args, **kwargs):
        stentor_slugify = stentor_conf.SLUGIFY
        if stentor_slugify is not None:
            if stentor_slugify:
                self.slug = stentor_slugify(self)
            else:
                self.slug = slugify(self.subject)
        now = timezone.now()
        self.update_date = now
        if not self.creation_date:
            self.creation_date = now
        super(Newsletter, self).save(*args, **kwargs)

    def get_absolute_url(self, sending=None):
        if sending:
            subscriber_hash = obfuscator.encode_web_view_hash(sending)
            url = reverse_lazy(
                'stentor:newsletter.subscriber_web_view',
                kwargs={
                    'newsletter_slug': self.slug,
                    'subscriber_hash': subscriber_hash
                },
                urlconf=stentor_conf.PUBLIC_URLCONF
            )
        else:
            url = reverse_lazy(
                'stentor:newsletter.anonymous_web_view',
                kwargs={'newsletter_slug': self.slug},
                urlconf=stentor_conf.PUBLIC_URLCONF
            )
        return url

    def schedule_sending(
            self, mailing_lists=None, subscribers=None, when=None):
        """
        Schedule the sending of this newsletter for the datetime ``when``.
        """
        self.clean()
        return ScheduledSending.objects.bulk_create_for(
            newsletter=self,
            mailing_lists=mailing_lists,
            subscribers=subscribers,
            when=when
        )

    def test_send_now(
            self, mailing_lists=None, subscribers=None, subject=''):
        """
        NOTE: This may be slow for large amount of emails. Avoid it and use
        only for testing.
        """
        if not subject:
            subject = self.subject

        emails = []
        emails += [sub.email for sub in mailing_lists.subscribers.active()]
        emails += [sub.email for sub in subscribers if sub.is_active()]

        for email in emails:
            send_mail(
                subject,
                self.email_html,  # TODO: This seems wrong
                stentor_conf.SENDER_VERBOSE,
                (self.subscriber.get_email(),)
            )

    def send_now(self, mailing_lists=None, subscribers=None):
        scheduled_sendings = self.schedule_sending()
        scheduled_sendings.send_and_delete()

    def get_email_tracker_url(self, sending):
        subscriber_hash = obfuscator.encode_email_tracker_hash(sending)
        return reverse_lazy(
            'stentor:newsletter.email_view_tracker',
            kwargs={
                'newsletter_slug': self.slug,
                'subscriber_hash': subscriber_hash
            },
            urlconf=stentor_conf.PUBLIC_URLCONF
        )

    @cached_property
    def html_template_paths(self):
        return stentor_conf.TEMPLATES[self.template]

    @cached_property
    def email_html_template_path(self):
        return self.html_template_paths[0]

    @cached_property
    def web_html_template_path(self):
        return self.html_template_paths[1]

    @cached_property
    def email_html_template(self):
        return get_template(self.email_html_template_path)

    @cached_property
    def web_html_template(self):
        return get_template(self.web_html_template_path)

    def get_mailing_lists(self):
        for mailing_list in self.mailing_lists.all():
            yield mailing_list

    def get_explicit_subscribers(self, active_only=True):
        subscribers = self.subscribers.all()
        if active_only:
            subscribers = subscribers.active()
        for subscriber in subscribers:
            yield subscriber

    def get_all_subscribers(self, distinct=True, active_only=True):
        distinct_subscribers = set()
        for mailing_list in self.get_mailing_lists():
            ml_subscribers = mailing_list.subscribers.all()
            if active_only:
                ml_subscribers = ml_subscribers.active()
            for subscriber in ml_subscribers:
                if not distinct:
                    yield subscriber
                else:
                    if subscriber not in distinct_subscribers:
                        yield subscriber
                        distinct_subscribers.add(subscriber)
        for subscriber in self.get_explicit_subscribers(active_only):
            if not distinct:
                yield subscriber
            else:
                if subscriber not in distinct_subscribers:
                    yield subscriber
                    distinct_subscribers.add(subscriber)

    @cached_property
    def email_html_first_phase_render(self):
        context = Context({
            'newsletter': self
        })
        return self.email_html_template.render(context)

    @cached_property
    def total_past_recipients(self):
        return len(self.past_recipients)
    total_past_recipients.short_description = _('Past recipients')

    @cached_property
    def total_email_impressions(self):
        return len(self.email_impressions)
    total_email_impressions.short_description = _('Email impressions')

    @cached_property
    def total_web_impressions(self):
        return len(self.web_impressions)
    total_web_impressions.short_description = _('Web impressions')

    @cached_property
    def total_pending_sendings(self):
        return self.scheduled_sendings.count()
    total_pending_sendings.short_description = _('Pending sendings')

    @cached_property
    def total_impressions(self):
        return chain(self.email_impressions, self.web_impressions)

    @cached_property
    def distinct_impressions(self):
        return set(chain(self.email_impressions, self.web_impressions))

    @cached_property
    def impression_rate(self):
        if not self.total_past_recipients:
            return 0
        return (self.total_impressions / self.total_past_recipients) * 100

    # Accepts subscriber instances or subscriber pks
    def add_impression(self, subscriber, impression_type):
        if not isinstance(subscriber, Subscriber):
            try:
                subscriber = Subscriber.objects.get(pk=subscriber)
            except Subscriber.DoesNotExist:
                raise ValueError(
                    'subscriber is neither a Subscriber instance nor a '
                    'pk of an existing Subscriber')
        if impression_type == 'email':
            self.email_impressions.append(subscriber)
        elif impression_type == 'web':
            self.web_impressions.append(subscriber)
        else:
            raise ValueError(
                'impression_type should be either "email" or "web"'
            )


@python_2_unicode_compatible
class ScheduledSending(models.Model):
    """
    A scheduled mailing for sending a newsletter to one subscriber.

    This is denormalized so as to make the sending of many emails per batch
    possible.

    In the current implementation a cron job is responsible for doing the
    actual sending.
    """
    subscriber = models.ForeignKey(Subscriber)
    newsletter = models.ForeignKey(Newsletter)
    sending_date = models.DateTimeField()
    message = models.TextField(blank=True)

    objects = stentor_managers.ScheduledSendingManager()

    class Meta:
        default_related_name = 'scheduled_sendings'
        verbose_name = 'scheduled sending of newsletter'
        verbose_name_plural = 'scheduled sendings of newslettters'

    def __str__(self):
        return u'Sending of %s to %s' % (self.newsletter, self.subscriber)

    def get_finalized_message(self, force_render=False):
        """
        Composes the message for the specific subscriber. Returns the message.
        """
        if force_render or not self.message:
            mail_template = Template(
                self.newsletter.email_html_first_phase_render
            )
            context_vars = {
                'newsletter': self.newsletter,
                'subscriber': self.subscriber,
                'sending': self,
            }
            context = Context(context_vars)
            self.message = mail_template.render(context)
        return self.message

    def get_common_email_data(self):
        return [
            self.newsletter.subject,
            self.get_finalized_message(),
            stentor_conf.SENDER_VERBOSE,
            (self.subscriber.get_email(),)
        ]

    def get_email_message(self):
        attrs = self.get_common_email_data()
        email_message = EmailMessage(*attrs)
        # Change the subtype to HTML, the common case for newsletters
        email_message.content_subtype = 'html'
        return email_message

    def send(self):
        """
        """
        email_message = self.get_email_message()
        sent = email_message.send()

        if not sent:
            self.handle_failed_sending(email_message)
        else:
            self.handle_successful_sending()
            self.delete()

        return sent

    def get_web_view_url(self):
        return self.newsletter.get_absolute_url(self)

    def get_email_tracker_url(self):
        return self.newsletter.get_email_tracker_url(self)
