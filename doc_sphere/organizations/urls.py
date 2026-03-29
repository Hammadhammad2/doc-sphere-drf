from django.urls import path

from .views import (
    OrganizationDetailAPIView,
    OrganizationInviteAcceptAPIView,
    OrganizationInviteCreateAPIView,
    OrganizationListCreateAPIView,
    OrganizationMemberRemoveAPIView,
    OrganizationMemberRoleUpdateAPIView,
)


app_name = "organizations"

urlpatterns = [
    path("", OrganizationListCreateAPIView.as_view(), name="list_organizations"),
    path("<int:pk>/", OrganizationDetailAPIView.as_view(), name="organization_detail"),
    path("<int:organization_id>/invites/", OrganizationInviteCreateAPIView.as_view(), name="create_invite"),
    path("invites/accept/<uuid:token>/", OrganizationInviteAcceptAPIView.as_view(), name="accept_invite"),
    path(
        "<int:organization_id>/members/<int:user_id>/",
        OrganizationMemberRemoveAPIView.as_view(),
        name="remove_member",
    ),
    path(
        "<int:organization_id>/members/<int:user_id>/role/",
        OrganizationMemberRoleUpdateAPIView.as_view(),
        name="update_member_role",
    ),
]
