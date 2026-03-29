from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Project(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="projects")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_projects",
    )

    def __str__(self):
        return self.name
