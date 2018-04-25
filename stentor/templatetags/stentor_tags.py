# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils import six

from stentor import settings as stentor_conf

if not stentor_conf.PUBLIC_SITE_URL:
    try:
        from django.contrib.sites.models import Site
    except ImportError:
        raise ImproperlyConfigured(
            'You must either set the STENTOR_PUBLIC_SITE_URL setting '
            'or have the django.contrib.sites app installed and set up.')
    else:
        public_site_url = 'https://' + Site.objects.get_current().domain
else:
    public_site_url = stentor_conf.PUBLIC_SITE_URL


register = template.Library()


# This does not use an inclusion tag, so we can ensure that the output does not
# have leading or trailing whitespaces, regardless of the template (and the
# code editor of the end user that may enforce a trailing whitespace).
@register.simple_tag(takes_context=True)
def web_view_url(context):
    if 'public_site_url' not in context:
        context['public_site_url'] = public_site_url
    ctx_dict = context.dicts[1]
    ctx = {key: value for key, value in six.iteritems(ctx_dict)}
    html = render_to_string('stentor/partials/web_view_url.html', ctx)
    return html.strip()


# This does not use an inclusion tag, so we can ensure that the output does not
# have leading or trailing whitespaces, regardless of the template (and the
# code editor of the end user that may enforce a trailing whitespace).
@register.simple_tag(takes_context=True)
def email_tracker_url(context):
    if 'public_site_url' not in context:
        context['public_site_url'] = public_site_url
    ctx_dict = context.dicts[1]
    ctx = {key: value for key, value in six.iteritems(ctx_dict)}
    html = render_to_string('stentor/partials/email_tracker_url.html', ctx)
    return html.strip()


@register.simple_tag(takes_context=True)
def unsubscribe_url(context):
    if 'public_site_url' not in context:
        context['public_site_url'] = public_site_url
    ctx_dict = context.dicts[1]
    ctx = {key: value for key, value in six.iteritems(ctx_dict)}
    html = render_to_string('stentor/partials/unsubscribe_url.html', ctx)
    return html.strip()
