import json

from django.contrib import admin
from django_google_maps import fields as map_fields
from django_google_maps import widgets as map_widgets

from .models import Truck, MenuItem, Review, ReviewLike, Visit, Tag, Live, TruckImage, TruckEvent


class TruckImageInline(admin.StackedInline):
    model = TruckImage

    fields = [
        'image',
        'caption',
    ]


class TruckEventInline(admin.TabularInline):
    model = TruckEvent


@admin.register(TruckEvent)
class TruckEventAdmin(admin.ModelAdmin):
    model = TruckEvent

    list_display = [
        '__str__',
        'truck',
        'title',
        'description',
        'start_time',
        'end_time',
    ]

    sortable_by = [
        'start_time',
        'end_time',
    ]

    list_filter = [
        'start_time',
    ]

    search_fields = [
        'truck',
        'title',
        'description',
    ]


class TruckAdmin(admin.ModelAdmin):
    exclude = ('live',)
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

    list_display = (
        'title',
        'owner',
        'address',
        'phone',
        'website',
        'available_for_catering'
    )

    list_filter = (
        'available_for_catering',
    )

    search_fields = (
        'title',
        'owner',
        'address',
        'phone',
        'website',
    )

    inlines = [
        TruckImageInline,
        TruckEventInline,
    ]

    model = Truck


class TagAdmin(admin.ModelAdmin):
    model = Tag

    list_display = (
        'title',
        'featured',
        'icon',
    )

    list_filter = (
        'featured',
    )

    sortable_by = (
        'title',
        'featured',
    )


class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem

    list_display = (
        'truck',
        'name',
        'description',
        'price',
        'featured',
    )

    list_filter = (
        'truck',
        'featured',
    )

    search_fields = (
        'truck',
        'name',
        'description',
    )

    sortable_by = (
        'price',
        'featured',
    )


class ReviewAdmin(admin.ModelAdmin):
    model = Review

    list_display = (
        'truck',
        'reviewer',
        'rating',
        'description',
        'post_created',
        'post_edited',
    )

    list_filter = (
        'post_created',
        'rating',
    )

    sortable_by = (
        'post_created',
        'rating',
    )

    search_fields = (
        'description',
        'reviewer',
        'truck',
    )


class ReviewLikeAdmin(admin.ModelAdmin):
    model = ReviewLike

    list_display = (
        'truck',
        'liked_by',
        'is_liked',
    )

    search_fields = (
        'liked_by',
        "truck",
    )

    list_filter = (
        'is_liked',
    )

    def truck(self, obj):
        return obj.review.truck


class VisitAdmin(admin.ModelAdmin):
    model = Visit

    list_display = (
        'truck',
        'visitor',
        'visited',
    )

    list_filter = (
        'visited',
    )

    search_fields = (
        'visitor',
    )

    sortable_by = (
        'truck',
        'visited',
    )


class LiveAdmin(admin.ModelAdmin):
    model = Live

    list_display = (
        'truck',
        'start_time',
        'end_time',
        'live',
        'live_time'
    )

    search_fields = (
        'truck',
    )

    date_hierarchy = 'start_time'


admin.site.register(Tag, TagAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewLike, ReviewLikeAdmin)
admin.site.register(Live, LiveAdmin)
