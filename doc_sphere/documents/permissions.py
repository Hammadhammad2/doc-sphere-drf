from rest_framework.permissions import SAFE_METHODS, BasePermission

from doc_sphere.organizations.choices import Role
from doc_sphere.organizations.models import UserOrganization
from doc_sphere.projects.models import Project


class IsDocumentMemberWithWriteRolePermission(BasePermission):
    message = "You do not have permission to perform this action for this organization."

    def has_permission(self, request, view):
        if request.method != "POST":
            return True

        project_id = request.data.get("project")
        if project_id is None:
            return False

        organization_id = Project.objects.filter(pk=project_id).values_list("organization_id", flat=True).first()
        if organization_id is None:
            return False

        return UserOrganization.objects.filter(
            organization_id=organization_id,
            user=request.user,
            role__in=(Role.OWNER, Role.ADMIN),
        ).exists()

    def has_object_permission(self, request, _view, obj):
        if request.method in SAFE_METHODS:
            return UserOrganization.objects.filter(
                organization=obj.project.organization,
                user=request.user,
            ).exists()

        return UserOrganization.objects.filter(
            organization=obj.project.organization,
            user=request.user,
            role__in=(Role.OWNER, Role.ADMIN),
        ).exists()
