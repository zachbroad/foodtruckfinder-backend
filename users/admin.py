from django.contrib import admin

from .models import User, SearchTerm, FavoriteTruck, Feedback


class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback

    list_display = (
        'user',
        'description',
        'created',
    )

    search_fields = (
        'user',
        'description',
    )

    list_filter = (
        'created',
    )

    date_hierarchy = 'created'


class FavoriteTruckAdmin(admin.ModelAdmin):
    model = FavoriteTruck

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


class SearchTermAdmin(admin.ModelAdmin):
    model = SearchTerm

    list_display = (
        'term',
        'user',
        'searched_on'
    )

    list_filter = (
        'searched_on',
    )

    search_fields = (
        'user',
        'term',
    )

    date_hierarchy = 'searched_on'


class UserAdmin(admin.ModelAdmin):
    model = User

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'profile_picture',
        'biography',
        'date_joined',
        'last_login',
        'is_admin',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
    )

    date_hierarchy = 'date_joined'

    list_filter = (
        'date_joined',
        'is_admin',
        'is_active',
    )


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FavoriteTruck, FavoriteTruckAdmin)
admin.site.register(SearchTerm, SearchTermAdmin)
admin.site.register(User, UserAdmin)

