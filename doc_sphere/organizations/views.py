from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from doc_sphere.organizations.choices import Role
from doc_sphere.organizations.models import Organization, UserOrganization
from doc_sphere.organizations.permissions import IsOrganizationMemberWithWriteRolePermission
from doc_sphere.organizations.serializers import OrganizationSerializer


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
