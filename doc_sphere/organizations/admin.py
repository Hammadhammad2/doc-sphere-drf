from django.contrib import admin

from .models import Organization, OrganizationInvite, UserOrganization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "modified")
    search_fields = ("name",)


@admin.register(UserOrganization)
class UserOrganizationAdmin(admin.ModelAdmin):
    list_display = ("organization", "user", "role", "created", "modified")
    search_fields = ("organization__name", "user__email")
    list_filter = ("role",)


@admin.register(OrganizationInvite)
class OrganizationInviteAdmin(admin.ModelAdmin):
    list_display = ("organization", "email", "role", "status", "expires_at", "created")
    search_fields = ("organization__name", "email")
    list_filter = ("status", "role")
