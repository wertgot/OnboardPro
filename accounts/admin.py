from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Company, EmployeeProfile, User


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')


class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    fk_name = 'user'
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'company', 'is_active')
    list_filter = ('role', 'company', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('OnboardPro', {'fields': ('company', 'role')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('OnboardPro', {'fields': ('company', 'role')}),
    )
    inlines = [EmployeeProfileInline]
