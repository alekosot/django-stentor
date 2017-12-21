# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.template.loader import render_to_string


register = template.Library()


# This does not use an inclusion tag, so we can ensure that the output does not
# have leading or trailing whitespaces, regardless of the template (and the
# code editor of the end user that may enforce a trailing whitespace).
@register.simple_tag(takes_context=True)
def web_view_url(context):
    html = render_to_string('stentor/partials/web_view_url.html', context)
    return html.strip()


# This does not use an inclusion tag, so we can ensure that the output does not
# have leading or trailing whitespaces, regardless of the template (and the
# code editor of the end user that may enforce a trailing whitespace).
@register.simple_tag(takes_context=True)
def email_tracker_url(context):
    html = render_to_string('stentor/partials/email_tracker_url.html', context)
    return html.strip()


@register.simple_tag(takes_context=True)
def unsubscribe_url(context):
    return context['subscriber'].get_unsubscribe_url()
