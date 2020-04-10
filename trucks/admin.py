from django.contrib import admin
import json
from django.contrib import admin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from .models import Truck, MenuItem, Menu, Review, Like, Visit


class TruckAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {
            'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap',
            'data-autocomplete-options': json.dumps({ 'types': ['geocode',
                'establishment'], 'componentRestrictions': {
                  'country': 'us'
              }
          })
      })}
    }

    model = Truck


class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem


class ReviewAdmin(admin.ModelAdmin):
    model = Review 

class LikeAdmin(admin.ModelAdmin):
    model = Like


class VisitAdmin(admin.ModelAdmin):
    model = Visit

admin.site.register(Visit, VisitAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Like, LikeAdmin)
