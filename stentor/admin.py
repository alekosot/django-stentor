from django.contrib import admin

from .actions import (
    send_keep_scheduled_email, send_delete_scheduled_email, schedule_sending)

from .models import (
    MailingList, Subscriber, Newsletter, ScheduledSending
)


class MailingListAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)


class SubscriberAdmin(admin.ModelAdmin):

    fields = ('user', 'email', 'mailing_lists', 'is_active',)
    list_display = ('user', 'email', 'is_active',)
    list_filter = ('is_active',)


class NewsletterAdmin(admin.ModelAdmin):

    fields = ('subject', 'template', 'mailing_lists', 'subscribers', 'slug')
    list_display = ('subject', 'email_views')
    actions = [schedule_sending]


class ScheduledSendingAdmin(admin.ModelAdmin):

    fields = ('subscriber', 'newsletter', 'sending_date', 'message')
    list_display = ('subscriber', 'newsletter', 'sending_date', 'message')
    actions = [send_keep_scheduled_email, send_delete_scheduled_email]


admin.site.register(MailingList, MailingListAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(ScheduledSending, ScheduledSendingAdmin)
