from django.contrib import admin

from .models import Truck, MenuItem, OpenningTime


class TruckAdmin(admin.ModelAdmin):
    model = Truck


class MenuAdmin(admin.ModelAdmin):
    model = MenuItem


class OpenningTimeAdmin(admin.ModelAdmin):
    model = OpenningTime

admin.site.register(OpenningTime, OpenningTimeAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(MenuItem, MenuAdmin)
