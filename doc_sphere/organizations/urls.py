from django.urls import path

from doc_sphere.organizations.views import (
    OrganizationInviteAcceptAPIView,
    OrganizationInviteCreateAPIView,
    OrganizationListCreateAPIView,
    OrganizationMemberRetrieveUpdateDestroyAPIView,
    OrganizationRetrieveUpdateAPIView,
)


app_name = "organizations"

urlpatterns = [
    path("", OrganizationListCreateAPIView.as_view(), name="organization_list_create"),
    path("<int:pk>/", OrganizationRetrieveUpdateAPIView.as_view(), name="organization_retrieve_update"),
    path(
        "<int:organization_id>/invites/",
        OrganizationInviteCreateAPIView.as_view(),
        name="organization_invite_create",
    ),
    path(
        "invites/accept/<uuid:token>/",
        OrganizationInviteAcceptAPIView.as_view(),
        name="organization_invite_accept",
    ),
    path(
        "<int:organization_id>/members/<int:member_id>/",
        OrganizationMemberRetrieveUpdateDestroyAPIView.as_view(),
        name="organization_member_retrieve_update_destroy",
    ),
]
