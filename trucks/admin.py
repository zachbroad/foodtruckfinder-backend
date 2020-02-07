from django.contrib import admin

from .models import Truck, MenuItem, MenuItemCombo, Menu, OpenningTime, Review


class TruckAdmin(admin.ModelAdmin):
    model = Truck


class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem

class MenuItemComboAdmin(admin.ModelAdmin):
    model = MenuItemCombo 

""" class MenuAdmin(admin.ModelAdmin):
    model = Menu """

class OpenningTimeAdmin(admin.ModelAdmin):
    model = OpenningTime

class ReviewAdmin(admin.ModelAdmin):
    model = Review 


''' admin.site.register(MenuItemCombo, MenuItemComboAdmin) '''
admin.site.register(OpenningTime, OpenningTimeAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(MenuItem, MenuItemAdmin)

admin.site.register(MenuItemCombo, MenuItemComboAdmin)
admin.site.register(Review, ReviewAdmin)