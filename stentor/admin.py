# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _

from .forms import ScheduleNewsletterForm
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
                'total_distinct_impressions', 'impression_rate_as_percentage',
                'total_distinct_unsubscriptions',
                'distinct_unsubscription_rate_as_percentage'
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
        'total_distinct_unsubscriptions',
        'distinct_unsubscription_rate_as_percentage'
    )
    actions = ('schedule_sending',)
    prepopulated_fields = {'slug': ('subject', )}
    readonly_fields = (
        'total_pending_sendings', 'total_past_recipients',
        'total_email_impressions', 'total_web_impressions',
        'total_distinct_impressions', 'impression_rate_as_percentage',
        'total_distinct_unsubscriptions',
        'distinct_unsubscription_rate_as_percentage'
    )

    def schedule_sending(self, request, queryset):
        form = None
        if 'add' in request.POST:
            form = ScheduleNewsletterForm(request.POST)

            if form.is_valid():
                chosen_date = form.cleaned_data['chosen_date']

                for newsletter in queryset:
                    newsletter.schedule_sending(when=chosen_date)

                newsletter_cnt = queryset.count()
                success_msg = "Successfully scheduled {} newsletter{}".format(
                    newsletter_cnt, '' if newsletter_cnt == 1 else 's')
                success_msg += " for {:%d %B %Y at %H:%M %p}.".format(
                    chosen_date)
                self.message_user(request, success_msg)
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = ScheduleNewsletterForm(initial={
                '_selected_action': request.POST.getlist(
                    admin.ACTION_CHECKBOX_NAME)
            })

        context = {
            'title': _("Choose sending date"),
            'newsletters': queryset,
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'site_url': '/',
            'has_permission': request.user.has_perm('stentor.add_newsletter'),
            'has_change_permission': self.has_change_permission(request)
        }
        context['adminform'] = helpers.AdminForm(
            form,
            list([(None, {'fields': form.base_fields})]),
            self.get_prepopulated_fields(request))

        return render(request, 'stentor/choose_sending_date_form.html', context)
    schedule_sending.short_description = (
        'Schedule the selected newsletters for sending'
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
