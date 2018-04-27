# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.template.loader import render_to_string
from django.utils import six

from stentor.utils import get_public_site_url


public_site_url = get_public_site_url()


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


@register.simple_tag(takes_context=True)
def generic_identifier(context):
    if 'sending' in context:
        hash = context['sending'].get_generic_identifier_hash()
    else:
        hash = '!-' + obfuscator.encode_unsubscribe_hash(context['subscriber'])
    return hash
