# -*- coding: utf-8 -*-
"""
TODO: ABSOLUTE MUST DO is adding the use of PermissionRequiredMixin, instead
of the more permissive login_required
"""

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic

# from .. import forms as stentor_forms
from ..models import Newsletter, Subscriber, MailingList, ScheduledSending


class ListViewMixin(object):
    page_kwarg = 'page'
    paginate_by = 20


# Newsletter views


@method_decorator(login_required, name='dispatch')
class NewsletterListView(ListViewMixin, generic.ListView):
    model = Newsletter
    template_name = 'newsletter_list.html'


@method_decorator(login_required, name='dispatch')
class NewsletterCreateView(generic.CreateView):
    model = Newsletter
    # form_class = stentor_forms.NewsletterForm
    template_name = 'newsletter_change.html'


@method_decorator(login_required, name='dispatch')
class NewsletterUpdateView(generic.CreateView):
    model = Newsletter
    # form_class = stentor_forms.NewsletterForm
    template_name = 'newsletter_change.html'


@method_decorator(login_required, name='dispatch')
class NewsletterDeleteView(generic.DeleteView):
    model = Newsletter
    template_name = 'newsletter_delete.html'


# Subscriber views

@method_decorator(login_required, name='dispatch')
class SubscriberListView(ListViewMixin, generic.ListView):
    model = Subscriber
    template_name = 'subscriber_list.html'


@method_decorator(login_required, name='dispatch')
class SubscriberCreateView(generic.CreateView):
    model = Subscriber
    # form_class = stentor_forms.SubscriberForm
    template_name = 'subscriber_change.html'


@method_decorator(login_required, name='dispatch')
class SubscriberUpdateView(generic.CreateView):
    model = Subscriber
    # form_class = stentor_forms.SubscriberForm
    template_name = 'subscriber_change.html'


@method_decorator(login_required, name='dispatch')
class SubscriberDeleteView(generic.DeleteView):
    model = Subscriber
    template_name = 'subscriber_delete.html'


# Mailing list views


@method_decorator(login_required, name='dispatch')
class MailingListListView(ListViewMixin, generic.ListView):
    model = MailingList
    template_name = 'mailing_list_list.html'


@method_decorator(login_required, name='dispatch')
class MailingListCreateView(generic.CreateView):
    model = MailingList
    # form_class = stentor_forms.MailingListForm
    template_name = 'mailing_list_change.html'


@method_decorator(login_required, name='dispatch')
class MailingListUpdateView(generic.CreateView):
    model = MailingList
    # form_class = stentor_forms.MailingListForm
    template_name = 'mailing_list_change.html'


@method_decorator(login_required, name='dispatch')
class MailingListDeleteView(generic.DeleteView):
    model = MailingList
    template_name = 'mailing_list_delete.html'


# Scheduled sending views


@method_decorator(login_required, name='dispatch')
class ScheduledSendingListView(ListViewMixin, generic.ListView):
    model = ScheduledSending
    template_name = 'scheduled_sending_list.html'


@method_decorator(login_required, name='dispatch')
class ScheduledSendingCreateView(generic.CreateView):
    model = ScheduledSending
    # form_class = stentor_forms.ScheduledSendingForm
    template_name = 'scheduled_sending_change.html'


@method_decorator(login_required, name='dispatch')
class ScheduledSendingUpdateView(generic.CreateView):
    model = ScheduledSending
    # form_class = stentor_forms.ScheduledSendingForm
    template_name = 'scheduled_sending_change.html'


@method_decorator(login_required, name='dispatch')
class ScheduledSendingDeleteView(generic.DeleteView):
    model = ScheduledSending
    template_name = 'scheduled_sending_delete.html'
