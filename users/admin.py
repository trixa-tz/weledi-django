from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_auditor', 'is_staff', 'is_superuser')
    list_filter = UserAdmin.list_filter + ('is_auditor',)
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('phone', 'is_auditor')}),
    )
