import json

from django.contrib import admin
from django_google_maps import fields as map_fields
from django_google_maps import widgets as map_widgets

from .models import Event


class EventAdmin(admin.ModelAdmin):
    model = Event

    list_display = [
        'title',
        'description',
        'start_time',
        'end_time',
        'address',
        'geolocation',
    ]

    fields = [
        'title',
        'description',
        'start_time',
        'end_time',
        'address',
        'geolocation',
        'trucks',
    ]

    list_filter = [
        'start_time',
        'end_time',
    ]

    sortable_by = [
        'start_time',
        'end_time',
    ]

    search_fields = [
        'title',
        'description',
        'address',
        'trucks',
    ]

    formfield_overrides = {
        map_fields.AddressField: {
            'widget': map_widgets.GoogleMapsAddressWidget(
                attrs={
                    'data-map-type':
                        'roadmap', 'data-autocomplete-options':
                        json.dumps({
                            'types': [
                                'geocode',
                                'establishment'
                            ],
                            'componentRestrictions':
                                {'country': 'us'}
                        })
                })
        }
    }


admin.site.register(Event, EventAdmin)
