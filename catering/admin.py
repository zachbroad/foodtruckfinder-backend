from django.contrib import admin

from catering.models import CaterRequest


class CaterRequestAdmin(admin.ModelAdmin):
    model = CaterRequest


admin.site.register(CaterRequest, CaterRequestAdmin)
