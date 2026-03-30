from rest_framework.permissions import SAFE_METHODS, BasePermission

from .choices import Role
from .models import UserOrganization


class IsOrganizationMemberWithWriteRolePermission(BasePermission):
    def has_object_permission(self, request, _view, obj):
        if request.method in SAFE_METHODS:
            return obj.members.filter(pk=request.user.pk).exists()

        return UserOrganization.objects.filter(
            organization=obj,
            user=request.user,
            role__in=(Role.OWNER, Role.ADMIN),
        ).exists()


class IsOrganizationAdminOrOwner(BasePermission):
    message = "Only organization admins or owners can perform this action."

    def has_permission(self, request, view):
        organization_id = view.kwargs.get("organization_id")

        return UserOrganization.objects.filter(
            organization_id=organization_id,
            user=request.user,
            role__in=(Role.OWNER, Role.ADMIN),
        ).exists()
