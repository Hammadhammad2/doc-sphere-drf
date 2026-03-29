from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Document(TimeStampedModel):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="documents")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_documents",
    )

    def __str__(self):
        return self.title
