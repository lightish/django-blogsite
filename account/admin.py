from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff', 'about')
    search_fields = ('username', 'email', 'about')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    filter_vertical = ()
    fieldsets = ()

    sortable_by = ('username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff')
