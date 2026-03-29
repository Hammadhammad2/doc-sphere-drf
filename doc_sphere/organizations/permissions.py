from rest_framework.permissions import SAFE_METHODS, BasePermission

from doc_sphere.organizations.choices import Role
from doc_sphere.organizations.models import UserOrganization


class IsOrganizationMemberWithWriteRolePermission(BasePermission):
    def has_object_permission(self, request, _view, obj):
        if request.method in SAFE_METHODS:
            return obj.members.filter(pk=request.user.pk).exists()

        return UserOrganization.objects.filter(
            organization=obj,
            user=request.user,
            role__in=(Role.OWNER, Role.ADMIN),
        ).exists()
