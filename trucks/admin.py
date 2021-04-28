import json

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django_google_maps import fields as map_fields
from django_google_maps import widgets as map_widgets

from .models import Truck, MenuItem, Review, ReviewLike, Visit, Tag, Live, TruckImage, TruckEvent, TruckFavorite


class TruckImageInline(admin.StackedInline):
    model = TruckImage

    fields = [
        'image',
        'caption',
    ]


class TruckEventInline(admin.TabularInline):
    model = TruckEvent


class FavoriteTruckAdmin(admin.ModelAdmin):
    model = TruckFavorite

    list_display = (
        'user',
        'truck',
        'created'
    )

    search_fields = (
        'user',
        'truck',
    )

    list_filter = (
        'created',
    )

    date_hierarchy = 'created'


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
        'available_for_catering',
        'image',
    )

    class HasImageFilter(admin.SimpleListFilter):
        title = 'has image'
        parameter_name = 'has_image'

        def lookups(self, request, model_admin):
            return [
                ('has_image', 'Has image'),
                ('has_default_image', 'Has default image'),
                ('has_no_image', 'Has no image')
            ]

        def queryset(self, request, queryset):
            if self.value() == 'has_image':
                return queryset.distinct().filter(image__isnull=False)
            elif self.value() == 'has_default_image':
                return queryset.distinct().filter(image=Truck._meta.get_field('image').get_default())
            elif self.value() == 'has_no_image':
                return queryset.distinct().filter(image__isnull=True)
            else:
                return queryset


    list_filter = (
        'available_for_catering',
        HasImageFilter
    )



    def has_image(self, obj):
        return obj.image != None

    has_image.boolean = True
    has_image.short_description = 'Find trucks without images.'

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


admin.site.register(Live, LiveAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewLike, ReviewLikeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(TruckFavorite, FavoriteTruckAdmin)
admin.site.register(Visit, VisitAdmin)
