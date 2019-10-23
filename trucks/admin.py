from django.contrib import admin

from .models import Truck, MenuItem


class TruckAdmin(admin.ModelAdmin):
    model = Truck


class MenuAdmin(admin.ModelAdmin):
    model = MenuItem


admin.site.register(Truck, TruckAdmin)
admin.site.register(MenuItem, MenuAdmin)
