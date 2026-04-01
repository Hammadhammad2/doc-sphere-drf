from django.urls import path

from .views import ProjectDetailAPIView, ProjectListCreateAPIView


app_name = "projects"

urlpatterns = [
    path("", ProjectListCreateAPIView.as_view(), name="list_projects"),
    path("<int:pk>/", ProjectDetailAPIView.as_view(), name="project_detail"),
]
