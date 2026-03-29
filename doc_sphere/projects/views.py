from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from doc_sphere.organizations.models import UserOrganization

from .models import Project
from .permissions import IsProjectMemberWithWriteRolePermission
from .serializers import ProjectSerializer


class ProjectListCreateAPIView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (IsProjectMemberWithWriteRolePermission,)
    search_fields = ("name",)

    def get_queryset(self):
        return Project.objects.filter(organization__members=self.request.user)

    def perform_create(self, serializer):
        organization = serializer.validated_data["organization"]

        is_member = UserOrganization.objects.filter(
            organization=organization,
            user=self.request.user,
        ).exists()

        if not is_member:
            raise ValidationError({"organization": "You are not a member of this organization."})

        serializer.save(created_by=self.request.user)


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (IsProjectMemberWithWriteRolePermission,)

    def get_queryset(self):
        return Project.objects.filter(organization__members=self.request.user)
