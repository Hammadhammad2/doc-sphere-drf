from rest_framework.permissions import SAFE_METHODS, BasePermission

from doc_sphere.organizations.choices import Role
from doc_sphere.organizations.models import UserOrganization


class IsOrganizationMemberWithWriteRolePermission(BasePermission):
    def has_permission(self, request, view):
        organization_id = view.kwargs.get("organization_id")

        if request.method in SAFE_METHODS:
            return UserOrganization.objects.filter(organization_id=organization_id, user=request.user).exists()

        return UserOrganization.objects.filter(
            organization_id=organization_id, user=request.user, role__in=(Role.OWNER, Role.ADMIN)
        ).exists()
