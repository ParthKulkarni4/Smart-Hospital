from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.shortcuts import render

from .models import RadiologyTest, RadiologyReport, RadiologyRecord
from .serializers import RadiologyTestSerializer, RadiologyReportSerializer, RadiologyRecordSerializer
from .permissions import CanManageTests, CanUploadRecords, CanCreateReport, ReportObjectPermission, in_group

def radiology_home(request):
    return render(request, "radiology/index.html")


class RadiologyTestViewSet(viewsets.ModelViewSet):
    queryset = RadiologyTest.objects.all()
    serializer_class = RadiologyTestSerializer
    permission_classes = [CanManageTests]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["modality", "is_active"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "code"]

class RadiologyReportViewSet(viewsets.ModelViewSet):
    queryset = RadiologyReport.objects.select_related("test", "created_by", "finalized_by").all()
    serializer_class = RadiologyReportSerializer
    permission_classes = [CanCreateReport, ReportObjectPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["test", "status", "created_by"]
    search_fields = ["patient_name", "findings", "test__name"]
    ordering_fields = ["created_at", "finalized_at"]

    def perform_create(self, serializer):
        user = self.request.user
        # Radiographers creating reports should be forced to 'draft'
        if in_group(user, "Radiographer"):
            serializer.save(created_by=user, status="draft")
        else:
            serializer.save(created_by=user)

    @action(detail=True, methods=["post"], url_path="finalize")
    def finalize(self, request, pk=None):
        """
        Mark a report as finalized. Only Radiologist or Admin/staff allowed.
        payload optional: {"findings": "...", "status": "final"}
        """
        report = self.get_object()
        user = request.user
        # check role
        allowed = user.is_staff or user.is_superuser or in_group(user, "Admin") or in_group(user, "Radiologist")
        if not allowed:
            return Response({"detail": "Only Radiologist or Admin may finalize reports."}, status=status.HTTP_403_FORBIDDEN)

        findings = request.data.get("findings")
        status_val = request.data.get("status", "final")
        if findings is not None:
            report.findings = findings
        report.status = status_val
        report.finalized_by = user
        report.finalized_at = timezone.now()
        report.save()
        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RadiologyRecordViewSet(viewsets.ModelViewSet):
    queryset = RadiologyRecord.objects.select_related("test", "report", "uploaded_by").all()
    serializer_class = RadiologyRecordSerializer
    permission_classes = [CanUploadRecords]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["test", "report"]
    search_fields = ["patient_name"]
    ordering_fields = ["uploaded_at"]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(uploaded_by=user)
