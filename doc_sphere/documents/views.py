from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from doc_sphere.organizations.models import UserOrganization

from .models import Document
from .permissions import IsDocumentMemberWithWriteRolePermission
from .serializers import DocumentSerializer


class DocumentListCreateAPIView(ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (IsDocumentMemberWithWriteRolePermission,)
    search_fields = ("title", "project__name")

    def get_queryset(self):
        return Document.objects.filter(project__organization__members=self.request.user)

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        is_member = UserOrganization.objects.filter(
            organization=project.organization,
            user=self.request.user,
        ).exists()
        if not is_member:
            raise ValidationError({"project": "You are not a member of this organization."})

        serializer.save(created_by=self.request.user)


class DocumentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (IsDocumentMemberWithWriteRolePermission,)

    def get_queryset(self):
        return Document.objects.filter(project__organization__members=self.request.user)
