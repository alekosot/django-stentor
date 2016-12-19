# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template


register = template.Library()


# TODO: Note the link to the docs concerning the handling of invalid variables:
# https://docs.djangoproject.com/en/1.9/ref/templates/api/#how-invalid-variables-are-handled  #NOQA
@register.inclusion_tag(
    'stentor/partials/web_view_url.html', takes_context=True)
def web_view_url(context):
    return context


@register.inclusion_tag(
    'stentor/partials/email_tracker_url.html', takes_context=True)
def email_tracker_url(context):
    return context
