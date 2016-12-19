# -*- coding: utf-8 -*-
# TODO: Check this module thoroughly.
"""
The views for all public facing urls of the application.
"""
from __future__ import unicode_literals

from datetime import datetime

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Template, Context
from django.utils import timezone
from django.utils.module_loading import import_string
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import CreateView

from .. import settings as stentor_conf
from .. import utils as stentor_utils

from ..models import Newsletter, Subscriber


TRANSPARENT_1_PIXEL_GIF = '\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'


class SubscriptionFormMixin(object):
    def form_valid(self, form):
        response = super(SubscriptionFormMixin, self).form_valid(form)
        if self.request.is_ajax:
            data = {
                'html': str(form),
                'email': self.form.cleaned_data['email']
            }
            return JsonResponse(data)
        return response

    def form_invalid(self, form):
        response = super(SubscriptionFormMixin, self).form_invalid(form)
        if self.request.is_ajax:
            data = {
                'html': form,
                'email': self.form.cleaned_data['email'],
                'errors': form.errors,
            }
            return JsonResponse(data, status=400)
        return response


def subscribe(request):
    SubscribeForm = import_string(stentor_conf.SUBSCRIBE_FORM)

    if request.method == 'POST':
        form = SubscribeForm(request, prefix='newsletter-subscribe')
        if form.is_valid():
            extra_tags = request.get('tags', '')
            extra_tags = extra_tags.split(',')
            for extra_tag in extra_tags:
                extra_tag = extra_tag.strip()
            form.save()
            if request.is_ajax():
                return render(
                    request, 'newsletter/subscribe_thanks_message.html')
            success_url = reverse('newsletter.subscribe_thanks')
            return redirect(request, success_url)
    else:
        form = SubscribeForm(prefix='newsletter-subscribe')

    if request.is_ajax():
        return render(
            request, 'newsletter/subscribe_form.html', {'form': form})

    return render(request, 'newsletter/subscribe.html', {'form': form})


# TODO: Check that this does not fail when the subscriber already exists
class SubscribeView(SubscriptionFormMixin, FormView):
    form_class = import_string(stentor_conf.SUBSCRIBE_FORM)
    success_url = reverse_lazy('stentor.subscriber.subscribe_success')
    template_name = 'stentor/subscribe.html'


class SubscribeSuccessView(TemplateView):
    template = 'stentor/subscribe_success.html'


class UnsubscribeView(SubscriptionFormMixin, FormView):
    form_class = import_string(stentor_conf.UNSUBSCRIBE_FORM)
    success_url = reverse_lazy('stentor.subscriber.unsubscribe_success')
    template_name = 'stentor/unsubscribe.html'

    def get_initial(self):
        initial = {
            'unsubscribe_hash': self.kwargs['unsubscribe_hash']
        }
        return initial


class UnsubscribeSuccessView(TemplateView):
    template = 'newsletter/unsubscribe_success.html'


def _newsletter_web_view(request, newsletter_slug, subscriber=None):
    newsletter = get_object_or_404(Newsletter, slug=newsletter_slug)
    newsletter.increment_web_views()
    is_anonymous_view = False if subscriber else True
    context_vars = {
        'newsletter': newsletter,
        'subscriber': subscriber,
        'is_anonymous_view': is_anonymous_view
    }
    template = Template(newsletter.web_html)
    context = Context(context_vars)
    output = template.render(context)
    return HttpResponse(output)


def newsletter_web_view_from_subscriber(
        request, newsletter_slug, subscriber_hash):
    subscriber_pk = stentor_utils.hasher.decode(subscriber_hash)[0]
    subscriber = get_object_or_404(Subscriber, pk=subscriber_pk)
    return _newsletter_web_view(request, newsletter_slug, subscriber)


def newsletter_web_view_from_anonymous(request, newsletter_slug):
    return _newsletter_web_view(request, newsletter_slug)


# TODO - Design-decision needed: This does nothing with the Subscriber
# instance, perhaps it should be more permissive?
def newsletter_email_tracker(request, newsletter_slug, subscriber_hash):
    newsletter = get_object_or_404(Newsletter, slug=newsletter_slug)
    subscriber_pk = stentor_utils.hasher.decode(subscriber_hash)[0]
    get_object_or_404(Subscriber, pk=subscriber_pk)
    newsletter.increment_email_views()
    return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type="image/gif")
