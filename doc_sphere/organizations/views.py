from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from doc_sphere.organizations.choices import InviteStatus, Role
from doc_sphere.organizations.models import Organization, OrganizationInvite, UserOrganization
from doc_sphere.organizations.permissions import (
    IsOrganizationAdminOrOwnerPermission,
    IsOrganizationMemberWithWriteRolePermission,
)
from doc_sphere.organizations.serializers import (
    OrganizationInviteCreateSerializer,
    OrganizationMemberRoleUpdateSerializer,
    OrganizationSerializer,
)


class OrganizationListCreateAPIView(ListCreateAPIView):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        organization = serializer.save()
        UserOrganization.objects.create(user=self.request.user, organization=organization, role=Role.OWNER)


class OrganizationRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = (IsOrganizationMemberWithWriteRolePermission,)

    def get_queryset(self):
        return Organization.objects.filter(members=self.request.user)


class OrganizationInviteCreateAPIView(CreateAPIView):
    serializer_class = OrganizationInviteCreateSerializer
    permission_classes = (IsOrganizationAdminOrOwnerPermission,)

    def get_organization(self):
        return get_object_or_404(Organization, pk=self.kwargs["organization_id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["organization"] = self.get_organization()
        return context

    def perform_create(self, serializer):
        organization = self.get_organization()
        invite = serializer.save(organization=organization, invited_by=self.request.user)
        self._send_invite_email(invite)

    def _send_invite_email(self, invite):
        accept_url = self.request.build_absolute_uri(
            reverse("organizations:organization_invite_accept", kwargs={"token": str(invite.token)})
        )

        subject = f"Invitation to join {invite.organization.name}"

        message = (
            f"You have been invited to join {invite.organization.name}.\n\n"
            f"Accept invite: {accept_url}\n"
            f"Invite expires at: {invite.expires_at.isoformat()}"
        )
        send_mail(subject, message, getattr(settings, "DEFAULT_FROM_EMAIL", None), [invite.email])


class OrganizationInviteAcceptAPIView(APIView):
    def post(self, request, token):
        invite = get_object_or_404(OrganizationInvite.objects.select_related("organization"), token=token)
        if invite.status != InviteStatus.PENDING:
            raise ValidationError("This invite is no longer valid.")

        if invite.expires_at <= timezone.now():
            invite.status = InviteStatus.EXPIRED
            invite.save(update_fields=["status", "modified"])
            raise ValidationError("This invite has expired.")

        if request.user.email.lower() != invite.email.lower():
            raise ValidationError("Invite email does not match the authenticated user.")

        UserOrganization.objects.get_or_create(
            organization=invite.organization,
            user=request.user,
            defaults={"role": invite.role},
        )

        invite.status = InviteStatus.ACCEPTED
        invite.save(update_fields=["status", "modified"])

        return Response({"detail": "Invite accepted successfully."}, status=status.HTTP_200_OK)


class OrganizationMemberDestroyAPIView(DestroyAPIView):
    permission_classes = (IsOrganizationAdminOrOwnerPermission,)

    def get_object(self):
        return get_object_or_404(
            UserOrganization,
            organization_id=self.kwargs["organization_id"],
            user_id=self.kwargs["user_id"],
        )


class OrganizationMemberRoleUpdateAPIView(UpdateAPIView):
    serializer_class = OrganizationMemberRoleUpdateSerializer
    permission_classes = (IsOrganizationAdminOrOwnerPermission,)

    def get_object(self):
        return get_object_or_404(
            UserOrganization,
            organization_id=self.kwargs["organization_id"],
            user_id=self.kwargs["user_id"],
        )
