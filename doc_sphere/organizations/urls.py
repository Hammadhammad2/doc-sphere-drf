from django.urls import path

from doc_sphere.organizations.views import (
    OrganizationListCreateAPIView,
    OrganizationRetrieveUpdateAPIView,
)


app_name = "organizations"

urlpatterns = [
    path("", OrganizationListCreateAPIView.as_view(), name="List_create_oeganizations"),
    path("<int:pk>/", OrganizationRetrieveUpdateAPIView.as_view(), name="organization_detail"),
]
