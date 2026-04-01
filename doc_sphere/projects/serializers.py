from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "description", "organization", "created_by", "created", "modified")
        read_only_fields = (
            "id",
            "created_by",
            "created",
            "modified",
        )

    def validate_name(self, value):
        normalized_name = value.strip()
        if not normalized_name:
            raise serializers.ValidationError("Project name is required.")
        return normalized_name
