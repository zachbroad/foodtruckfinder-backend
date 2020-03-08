from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin

from .models import Account, SearchTerm, FavoriteTruck

admin.site.register(FavoriteTruck)
admin.site.register(SearchTerm)
admin.site.register(Account)
