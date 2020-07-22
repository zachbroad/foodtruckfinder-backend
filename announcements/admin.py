from django.contrib import admin

from .models import Announcement, AnnouncementImage


class AnnouncementImageAdmin(admin.TabularInline):
    model = AnnouncementImage


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'posted_on',
        'edited_on',
    ]

    sortable_by = [
        'posted_on',
        'edited_on',
    ]

    list_filter = [
        'posted_on',
        'edited_on',
    ]

    inlines = [
        AnnouncementImageAdmin,
    ]
