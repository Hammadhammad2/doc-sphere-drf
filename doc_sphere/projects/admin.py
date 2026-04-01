from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "created_by", "created", "modified")
    search_fields = ("name", "organization__name", "created_by__email")
    list_filter = ("organization", "created")
    ordering = ("-created",)
