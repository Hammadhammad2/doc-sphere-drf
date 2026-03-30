from django.urls import path

from doc_sphere.organizations.views import (
    OrganizationDetailAPIView,
    OrganizationListCreateAPIView,
)


app_name = "organizations"

urlpatterns = [
    path("", OrganizationListCreateAPIView.as_view(), name="list_organizations"),
    path("<int:pk>/", OrganizationDetailAPIView.as_view(), name="organization_detail"),
]
