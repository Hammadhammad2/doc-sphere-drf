from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "created_by", "created", "modified")
    search_fields = ("title", "project__name", "created_by__email")
    list_filter = ("project", "created")
    ordering = ("-created",)
