from django.contrib import admin

from .models import Truck, MenuItem, OpenningTime


class TruckAdmin(admin.ModelAdmin):
    model = Truck


class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem

''' class MenuItemComboAdmin(admin.ModelAdmin):
    model = MenuItemCombo '''


class OpenningTimeAdmin(admin.ModelAdmin):
    model = OpenningTime


''' admin.site.register(MenuItemCombo, MenuItemComboAdmin) '''
admin.site.register(OpenningTime, OpenningTimeAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
