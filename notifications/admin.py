from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'posted_on',
    ]

    search_fields = [
        'title',
        'description',
    ]

    sortable_by = [
        'posted_on',
    ]

    list_filter = [
        'posted_on',
    ]


