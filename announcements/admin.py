from django.contrib import admin

from .models import Announcement, AnnouncementImage
from markdownx.admin import MarkdownxModelAdmin


class AnnouncementImageAdmin(admin.TabularInline):
    model = AnnouncementImage


@admin.register(Announcement)
class AnnouncementAdmin(MarkdownxModelAdmin):
    list_display = [
        'title',
        'body',
        'posted_on',
        'edited_on',
    ]

    search_fields = [
        'title',
        'body',
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
