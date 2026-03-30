from rest_framework import serializers

from doc_sphere.organizations.choices import Role
from doc_sphere.organizations.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("id", "name", "description")

    def validate_name(self, value):
        user = self.context["request"].user
        normalized_name = value.strip()

        user_organizations = Organization.objects.filter(
            user_organizations__user=user,
            user_organizations__role=Role.OWNER,
            name__iexact=normalized_name,
        )

        if user_organizations.exists():
            raise serializers.ValidationError("You already have an organization with this name.")

        return normalized_name
