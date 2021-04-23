from django.contrib import admin

from catering.models import CaterRequest


class CaterRequestAdmin(admin.ModelAdmin):
    model = CaterRequest
    search_fields = (
        'name',
        'email',
        'truck',
        'details',
    )

    list_display = (
        'email',
        'name',
        'details',
        'status',
        'truck',
        'when',
        'requested_on',
        'duration',
    )

    list_filter = (
        'when',
        'status',
    )

    date_hierarchy = 'when'

    def when(self, obj):
        return '{} hours'.format(obj.when)


admin.site.register(CaterRequest, CaterRequestAdmin)
