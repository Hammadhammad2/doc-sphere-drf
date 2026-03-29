from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "title", "content", "project", "created_by", "created", "modified")
        read_only_fields = ("id", "created_by", "created", "modified")

    def validate_title(self, value):
        normalized_title = value.strip()
        if not normalized_title:
            raise serializers.ValidationError("Document title is required.")
        return normalized_title

    def validate(self, attrs):
        if self.instance is not None and "project" in attrs and attrs["project"] != self.instance.project:
            raise serializers.ValidationError({"project": "Document project cannot be changed."})
        return attrs
