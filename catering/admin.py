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
        'name',
        'email',
        'truck',
        'when',
        'duration',
    )

    date_hierarchy = 'when'

    def when(self, obj):
        return '{} hours'.format(obj.when)


admin.site.register(CaterRequest, CaterRequestAdmin)
