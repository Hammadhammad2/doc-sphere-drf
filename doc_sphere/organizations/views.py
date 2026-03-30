from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from doc_sphere.organizations.choices import Role
from doc_sphere.organizations.models import Organization, OrganizationInvite, UserOrganization
from doc_sphere.organizations.permissions import (
    IsOrganizationAdminOrOwner,
    IsOrganizationMemberWithWriteRolePermission,
)
from doc_sphere.organizations.serializers import (
    OrganizationInviteAcceptSerializer,
    OrganizationInviteCreateSerializer,
    OrganizationSerializer,
    UserOrganizationUpdateSerializer,
)
from doc_sphere.organizations.tasks import send_email_task


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
    permission_classes = (IsOrganizationAdminOrOwner,)

    def get_object(self):
        return get_object_or_404(Organization, pk=self.kwargs["organization_id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["organization"] = self.get_object()
        return context

    def perform_create(self, serializer):
        organization = self.get_object()
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

        send_email_task.delay(
            subject=subject,
            message=message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[invite.email],
        )


class OrganizationInviteAcceptAPIView(APIView):
    def post(self, request, token):
        invite = get_object_or_404(OrganizationInvite.objects.select_related("organization"), token=token)
        serializer = OrganizationInviteAcceptSerializer(
            data={},
            context={"request": request, "invite": invite},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Invite accepted successfully."}, status=status.HTTP_200_OK)


class OrganizationMemberRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserOrganizationUpdateSerializer
    permission_classes = (IsOrganizationAdminOrOwner,)

    def get_object(self):
        return get_object_or_404(
            UserOrganization,
            organization_id=self.kwargs["organization_id"],
            user_id=self.kwargs["member_id"],
        )
