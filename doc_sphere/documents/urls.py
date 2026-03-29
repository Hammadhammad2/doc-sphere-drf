from django.urls import path

from .views import DocumentDetailAPIView, DocumentListCreateAPIView


app_name = "documents"

urlpatterns = [
    path("", DocumentListCreateAPIView.as_view(), name="list_documents"),
    path("<int:pk>/", DocumentDetailAPIView.as_view(), name="document_detail"),
]
