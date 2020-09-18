from django.contrib import admin

from catering.models import CaterRequest


class CaterRequestAdmin(admin.ModelAdmin):
    model = CaterRequest
    search_fields = (
        'name',
        'email',
        'truck',
    )

    list_display = (
        'email',
        'details',
        'name',
        'truck',
        'when',
        'duration',
        'requested_on',
    )

    list_filter = (
        'when',
    )

    date_hierarchy = 'when'

    def when(self, obj):
        return '{} hours'.format(obj.when)


admin.site.register(CaterRequest, CaterRequestAdmin)
