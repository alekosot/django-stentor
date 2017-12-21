# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import MailingList, Subscriber, Newsletter, ScheduledSending


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
            # TODO: Add description here, for further info about how to use
            # this and what extra variables can be used
            'fields': (
                'total_pending_sendings', 'total_past_recipients',
                'total_email_impressions', 'total_web_impressions', 'impression_rate'
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
        'total_email_impressions', 'total_web_impressions', 'impression_rate',
    )
    actions = ('schedule_sending',)
    prepopulated_fields = {'slug': ('subject', )}
    readonly_fields = (
        'total_pending_sendings', 'total_past_recipients',
        'total_email_impressions', 'total_web_impressions', 'impression_rate'
    )

    def schedule_sending(self, request, queryset):
        for newsletter in queryset:
            newsletter.schedule_sending()
    schedule_sending.short_description = (
        'Schedule the selected newsletters for sending (as soon as possible)'
    )


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
