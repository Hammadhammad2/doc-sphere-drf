from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from .choices import Role
from .models import Organization, UserOrganization
from .permissions import IsOrganizationMemberWithWriteRolePermission
from .serializers import OrganizationSerializer


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
