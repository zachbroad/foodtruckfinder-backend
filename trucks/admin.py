from django.contrib import admin

from .models import Truck, MenuItem, Menu, OpenningTime, Review, Like


class TruckAdmin(admin.ModelAdmin):
    model = Truck


class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem

class OpenningTimeAdmin(admin.ModelAdmin):
    model = OpenningTime

class ReviewAdmin(admin.ModelAdmin):
    model = Review 

class LikeAdmin(admin.ModelAdmin):
    model = Like

admin.site.register(OpenningTime, OpenningTimeAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Like, LikeAdmin)
