from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin

from .models import User, SearchTerm, FavoriteTruck, Feedback

admin.site.register(Feedback)
admin.site.register(FavoriteTruck)
admin.site.register(SearchTerm)
admin.site.register(User)
