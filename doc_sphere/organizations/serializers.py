from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .choices import InviteStatus, Role
from .models import Organization, OrganizationInvite, UserOrganization


User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(trim_whitespace=True)

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
        if self.instance is not None:
            user_organizations = user_organizations.exclude(pk=self.instance.pk)

        if user_organizations.exists():
            raise serializers.ValidationError("You already have an organization with this name.")

        return normalized_name


class OrganizationInviteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationInvite
        fields = ("id", "email", "role", "status", "expires_at", "token")
        read_only_fields = ("id", "status", "expires_at", "token")

    def validate_email(self, value):
        return value.strip().lower()

    def validate(self, attrs):
        organization = self.context["organization"]
        email = attrs["email"]

        invite_exists = OrganizationInvite.objects.filter(
            organization=organization,
            email__iexact=email,
            status=InviteStatus.PENDING,
            expires_at__gt=timezone.now(),
        ).exists()

        if invite_exists:
            raise serializers.ValidationError({"email": "A pending invite already exists for this user."})

        user = User.objects.filter(email__iexact=email).first()

        if user is not None and UserOrganization.objects.filter(organization=organization, user=user).exists():
            raise serializers.ValidationError({"email": "This user is already a member of the organization."})

        return attrs


class OrganizationMemberRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOrganization
        fields = ("role",)

    def validate_role(self, value):
        if value == Role.OWNER:
            raise serializers.ValidationError("Owner role cannot be assigned from this endpoint.")
        return value
