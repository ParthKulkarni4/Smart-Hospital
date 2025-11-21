from django.contrib import admin


# ant to chnage

# Register your models here.

from .models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'admin_owner', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'role')
    list_filter = ('role', 'is_active', 'is_staff')