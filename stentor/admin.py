# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from . import settings as stentor_conf
from .models import MailingList, Subscriber, Newsletter, ScheduledSending
from .utils import TEMPLATE_CHOICES


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    fields = ('user', 'email', 'mailing_lists', 'is_active')
    list_display = ('email', 'user', 'is_active')
    list_filter = ('is_active',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'subject', 'slug', 'template', 'mailing_lists', 'subscribers'
            )
        }),
        ('Statistics', {
            'fields': (
                'total_pending_sendings', 'total_past_recipients',
                'total_email_impressions', 'total_web_impressions',
                'total_distinct_impressions', 'impression_rate_as_percentage'
            ),
        }),
        ('Custom HTML', {
            'classes': ('collapse',),
            # TODO: Add description here, for further info about how to use
            # this and what extra variables can be used
            'fields': ('custom_email_html', 'custom_web_html'),
        }),
    )
    list_display = (
        'subject', 'slug', 'total_pending_sendings', 'total_past_recipients',
        'total_email_impressions', 'total_web_impressions',
        'total_distinct_impressions', 'impression_rate_as_percentage',
    )
    actions = ('schedule_sending',)
    prepopulated_fields = {'slug': ('subject', )}
    readonly_fields = (
        'total_pending_sendings', 'total_past_recipients',
        'total_email_impressions', 'total_web_impressions',
        'total_distinct_impressions', 'impression_rate_as_percentage'
    )

    def schedule_sending(self, request, queryset):
        for newsletter in queryset:
            newsletter.schedule_sending()
    schedule_sending.short_description = (
        'Schedule the selected newsletters for sending (as soon as possible)'
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'template':
            return forms.ChoiceField(choices=TEMPLATE_CHOICES)
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(ScheduledSending)
class ScheduledSendingAdmin(admin.ModelAdmin):
    fields = ('subscriber', 'newsletter', 'sending_date', 'message')
    list_display = ('subscriber', 'newsletter', 'sending_date', 'message')
    actions = ('send', 'send_and_delete')

    def send(self, request, queryset):
        queryset.send()
    send.short_description = (
        'Send selected scheduled sendings (without deleting them)'
    )

    def send_and_delete(self, request, queryset):
        queryset.send_and_delete()
    send_and_delete.short_description = (
        'Send and delete selected scheduled sendings'
    )
