def send_keep_scheduled_email(modeladmin, request, queryset):
    queryset.send()
send_keep_scheduled_email.short_description = (
    "Send and keep selected scheduled emails")


def send_delete_scheduled_email(modeladmin, request, queryset):
    queryset.send_and_delete()
send_delete_scheduled_email.short_description = (
    "Send and delete  selected scheduled emails")


def schedule_sending(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.schedule_sending()
schedule_sending.short_description = (
    "Schedule selected newsletters for sending")
