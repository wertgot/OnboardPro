from django.http import FileResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import RoleChoices
from onboardpro.permissions import IsHR

from .models import Document
from .serializers import DocumentSerializer, DocumentSignSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Document.objects.filter(
            uploaded_by__company=self.request.user.company
        ).select_related('uploaded_by', 'task_progress')
        if self.request.user.role == RoleChoices.EMPLOYEE:
            return qs.filter(uploaded_by=self.request.user)
        return qs

    def get_permissions(self):
        if self.action in ('create', 'sign'):
            return [IsAuthenticated()]
        if self.request.user.role == RoleChoices.EMPLOYEE:
            return [IsAuthenticated()]
        return [IsHR()]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=['get'], url_path='file')
    def download_file(self, request, pk=None):
        doc = self.get_object()
        if request.user.role == RoleChoices.EMPLOYEE and doc.uploaded_by_id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return FileResponse(doc.file.open('rb'), as_attachment=True, filename=doc.file.name)

    @action(detail=True, methods=['post'])
    def sign(self, request, pk=None):
        doc = self.get_object()
        if doc.uploaded_by_id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = DocumentSignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doc.signature = serializer.validated_data['signature']
        doc.is_signed = True
        doc.save(update_fields=['signature', 'is_signed'])
        return Response(DocumentSerializer(doc).data)
